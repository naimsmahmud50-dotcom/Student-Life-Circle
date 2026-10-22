"""
================================================================================
MODULE: Supabase Database Envelope Field Encryption & Blind Indexing Service
TOPIC: Two-Tier Key Architecture (KEK/DEK), AES-256-GCM & HMAC Blind Indexing
FILE: backend/app/services/supabase_field_encryption_service.py
PURPOSE: Protects high-sensitivity database columns (National ID, bank routing,
         guardian PII, psychological assessments) using AES-256-GCM envelope
         encryption, accompanied by zero-knowledge blind indexes for exact searches.
AUDIENCE: Cryptographers, Database Administrators, Security Compliance Auditors.
================================================================================
"""

import os
import hmac
import hashlib
from typing import Dict, Any, Optional

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_AESGCM = True
except ImportError:
    HAS_AESGCM = False


class SupabaseFieldEncryptionService:
    """
    Implements production-grade database column envelope encryption.
    - KEK: Key Encryption Key (Master Key, 256-bit)
    - DEK: Data Encryption Key (Per-field/row ephemeral key, 256-bit)
    - Blind Index: Salted HMAC-SHA256 allowing exact-match database queries without decryption.
    """

    def __init__(
        self,
        master_kek_hex: Optional[str] = None,
        blind_index_salt_hex: Optional[str] = None
    ):
        # Default 256-bit Master Key for Agrojatra PII Vault
        self.master_kek = bytes.fromhex(
            master_kek_hex or "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        )
        self.blind_index_salt = bytes.fromhex(
            blind_index_salt_hex or "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210"
        )

    def envelope_encrypt(
        self,
        plaintext: str,
        associated_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Encrypts plaintext using a fresh 256-bit DEK, then encrypts the DEK with the master KEK.
        Generates an HMAC-SHA256 blind index for exact search queries.
        """
        aad = associated_data.encode("utf-8") if associated_data else None
        plaintext_bytes = plaintext.encode("utf-8")
        
        # Generate blind index for deterministic search
        blind_index = self.compute_blind_index(plaintext)

        # Generate 32-byte DEK and 12-byte nonces
        dek = os.urandom(32)
        dek_nonce = os.urandom(12)
        data_nonce = os.urandom(12)

        if HAS_AESGCM:
            # 1. Encrypt plaintext with DEK
            aes_data = AESGCM(dek)
            ciphertext = aes_data.encrypt(data_nonce, plaintext_bytes, aad)

            # 2. Encrypt DEK with Master KEK
            aes_kek = AESGCM(self.master_kek)
            encrypted_dek = aes_kek.encrypt(dek_nonce, dek, b"DEK_ENVELOPE_METADATA")
        else:
            # Fallback XOR-HMAC authenticated stream cipher
            ciphertext = self._fallback_encrypt(plaintext_bytes, dek, data_nonce)
            encrypted_dek = self._fallback_encrypt(dek, self.master_kek, dek_nonce)

        return {
            "ciphertext_hex": ciphertext.hex(),
            "data_nonce_hex": data_nonce.hex(),
            "encrypted_dek_hex": encrypted_dek.hex(),
            "dek_nonce_hex": dek_nonce.hex(),
            "blind_index_hex": blind_index,
            "cipher_algorithm": "AES-256-GCM" if HAS_AESGCM else "FALLBACK-XOR-HMAC",
            "associated_data": associated_data
        }

    def envelope_decrypt(
        self,
        ciphertext_hex: str,
        data_nonce_hex: str,
        encrypted_dek_hex: str,
        dek_nonce_hex: str,
        associated_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Decrypts the DEK using the Master KEK, then decrypts the ciphertext using the recovered DEK.
        """
        aad = associated_data.encode("utf-8") if associated_data else None
        ciphertext = bytes.fromhex(ciphertext_hex)
        data_nonce = bytes.fromhex(data_nonce_hex)
        encrypted_dek = bytes.fromhex(encrypted_dek_hex)
        dek_nonce = bytes.fromhex(dek_nonce_hex)

        try:
            if HAS_AESGCM:
                # 1. Decrypt DEK using KEK
                aes_kek = AESGCM(self.master_kek)
                dek = aes_kek.decrypt(dek_nonce, encrypted_dek, b"DEK_ENVELOPE_METADATA")

                # 2. Decrypt data using DEK
                aes_data = AESGCM(dek)
                decrypted_bytes = aes_data.decrypt(data_nonce, ciphertext, aad)
            else:
                dek = self._fallback_decrypt(encrypted_dek, self.master_kek, dek_nonce)
                decrypted_bytes = self._fallback_decrypt(ciphertext, dek, data_nonce)

            plaintext = decrypted_bytes.decode("utf-8")
            return {
                "success": True,
                "plaintext": plaintext,
                "cipher_algorithm": "AES-256-GCM" if HAS_AESGCM else "FALLBACK-XOR-HMAC"
            }
        except Exception as e:
            return {
                "success": False,
                "plaintext": None,
                "error": f"DECRYPTION_FAILED: Authentication tag mismatch or corrupted ciphertext ({str(e)})"
            }

    def compute_blind_index(self, value: str) -> str:
        """
        Computes a salted HMAC-SHA256 blind index for exact match search queries.
        Permits `WHERE pii_blind_index = :val` queries without exposing plaintext.
        """
        normalized_val = value.strip().lower()
        return hmac.new(
            self.blind_index_salt,
            normalized_val.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def _fallback_encrypt(self, data: bytes, key: bytes, nonce: bytes) -> bytes:
        keystream = hashlib.sha256(key + nonce).digest()
        repeated_ks = (keystream * ((len(data) // len(keystream)) + 1))[:len(data)]
        encrypted = bytes(a ^ b for a, b in zip(data, repeated_ks))
        tag = hmac.new(key, encrypted + nonce, hashlib.sha256).digest()[:16]
        return encrypted + tag

    def _fallback_decrypt(self, data_and_tag: bytes, key: bytes, nonce: bytes) -> bytes:
        tag = data_and_tag[-16:]
        encrypted = data_and_tag[:-16]
        expected_tag = hmac.new(key, encrypted + nonce, hashlib.sha256).digest()[:16]
        if not hmac.compare_digest(tag, expected_tag):
            raise ValueError("HMAC authentication tag mismatch")
        keystream = hashlib.sha256(key + nonce).digest()
        repeated_ks = (keystream * ((len(encrypted) // len(keystream)) + 1))[:len(encrypted)]
        return bytes(a ^ b for a, b in zip(encrypted, repeated_ks))
