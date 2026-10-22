/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - CHILD SAFETY UI:
 * MODULE:    Guardian Consent & Minor Profile Protection Card
 * TOPIC:     1-Click Guardian Verification, Minor Privacy Lockdown & Status Pills
 * FILE:      frontend/src/components/auth/GuardianConsentCard.tsx
 * PURPOSE:   Provides an interactive card interface for minor learners (age < 16) to
 *            link their legal guardian's phone number and dispatch affirmative consent SMS.
 *            Displays live privacy lockdown status, messaging restriction indicators,
 *            and strict ZERO-EMOJI compliance using Lucide SVG icons.
 * AUDIENCE:  Frontend Engineers, Child Protection Officers & UI Testers
 * STANDARDS: UI/UX Pro Max, ASVS L2 Child Privacy, Zero-Emoji Policy
 * ========================================================================================
 */

import React, { useState } from 'react';
import { 
  ShieldCheck, 
  ShieldAlert, 
  Lock, 
  Phone, 
  ExternalLink, 
  Clock, 
  UserCheck, 
  CheckCircle2, 
  AlertCircle, 
  RefreshCw 
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

export interface GuardianConsentCardProps {
  studentId: string;
  studentName: string;
  studentAge: number;
  initialConsentStatus?: 'PENDING' | 'APPROVED' | 'REVOKED' | 'NONE';
  initialGuardianPhone?: string;
  onConsentUpdated?: (status: string) => void;
}

export const GuardianConsentCard: React.FC<GuardianConsentCardProps> = ({
  studentId,
  studentName,
  studentAge,
  initialConsentStatus = 'NONE',
  initialGuardianPhone = '',
  onConsentUpdated
}) => {
  const [guardianPhone, setGuardianPhone] = useState<string>(initialGuardianPhone);
  const [status, setStatus] = useState<string>(initialConsentStatus);
  const [consentLink, setConsentLink] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const isMinor = studentAge < 16;

  const handleRequestConsent = async () => {
    if (!guardianPhone.trim()) {
      setErrorMessage('Please provide a valid guardian phone number.');
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const res = await fetch('/api/v1/auth-otp/guardian/request-consent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_id: studentId,
          student_name: studentName,
          guardian_phone: guardianPhone,
          student_age: studentAge
        })
      });

      const data = await res.json();
      if (!res.ok) {
        setErrorMessage(data.detail || 'Failed to dispatch guardian verification SMS.');
      } else {
        setStatus('PENDING');
        setConsentLink(data.consent_link || null);
        setSuccessMessage('Verification SMS dispatched to guardian successfully.');
        if (onConsentUpdated) onConsentUpdated('PENDING');
      }
    } catch {
      setErrorMessage('Network connection error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSimulateGuardianApproval = async () => {
    if (!consentLink) return;
    const url = new URL(consentLink);
    const token = url.searchParams.get('token');
    if (!token) return;

    setIsLoading(true);
    try {
      const res = await fetch('/api/v1/auth-otp/guardian/grant-consent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, relationship: 'PARENT' })
      });
      const data = await res.json();
      if (res.ok) {
        setStatus('APPROVED');
        setSuccessMessage('Guardian consent verified and active. Profile privacy lock lifted.');
        if (onConsentUpdated) onConsentUpdated('APPROVED');
      }
    } catch {
      setErrorMessage('Failed to simulate approval.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRevokeConsent = async () => {
    setIsLoading(true);
    try {
      const res = await fetch('/api/v1/auth-otp/guardian/revoke-consent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_id: studentId,
          guardian_phone: guardianPhone,
          reason: 'Guardian requested profile privacy re-lock.'
        })
      });
      if (res.ok) {
        setStatus('REVOKED');
        setSuccessMessage('Consent revoked. Profile locked to private mode.');
        if (onConsentUpdated) onConsentUpdated('REVOKED');
      }
    } catch {
      setErrorMessage('Failed to revoke consent.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full rounded-2xl bg-white border border-slate-200 shadow-sm overflow-hidden p-6 space-y-6">
      {/* Header with Child Safety Badge */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-4 border-b border-slate-100">
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-blue-50 text-blue-600">
            <Lock className="w-5 h-5" aria-hidden="true" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-slate-900">
              Child Protection & Guardian Consent
            </h3>
            <p className="text-xs text-slate-500">
              Student Age: {studentAge} years old &bull; Mandatory for learners under 16
            </p>
          </div>
        </div>

        {/* Dynamic Status Pill */}
        <div>
          {status === 'APPROVED' && (
            <Badge variant="verified" className="bg-teal-50 text-teal-700 border-teal-200">
              <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-teal-600" />
              Consent Approved
            </Badge>
          )}
          {status === 'PENDING' && (
            <Badge variant="outline" className="bg-amber-50 text-amber-700 border-amber-200">
              <Clock className="w-3.5 h-3.5 mr-1 text-amber-600" />
              Pending Guardian SMS
            </Badge>
          )}
          {status === 'REVOKED' && (
            <Badge variant="destructive" className="bg-rose-50 text-rose-700 border-rose-200">
              <ShieldAlert className="w-3.5 h-3.5 mr-1 text-rose-600" />
              Consent Revoked
            </Badge>
          )}
          {status === 'NONE' && (
            <Badge variant="outline" className="bg-slate-100 text-slate-600 border-slate-200">
              <Lock className="w-3.5 h-3.5 mr-1 text-slate-500" />
              Action Required
            </Badge>
          )}
        </div>
      </div>

      {/* Child Safety Privacy Notice */}
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 space-y-2">
        <div className="flex items-center space-x-2 text-slate-800 text-sm font-semibold">
          <ShieldCheck className="w-4 h-4 text-blue-600" />
          <span>Platform Minor Protection Policy</span>
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          {status === 'APPROVED' ? (
            'Guardian consent is active. Student can participate in verified study circles, communicate with verified tutors, and access full learning features under protective privacy monitoring.'
          ) : (
            'To protect minors, profiles without verified guardian consent remain strictly private. The profile is hidden from public searches and cannot receive unsolicited direct messages from unverified adult users.'
          )}
        </p>
      </div>

      {/* Input Form */}
      {status !== 'APPROVED' ? (
        <div className="space-y-4">
          <label className="block text-xs font-semibold text-slate-700">
            Parent or Legal Guardian Mobile Number
          </label>
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <Phone className="w-4 h-4" />
              </div>
              <input
                type="tel"
                value={guardianPhone}
                onChange={(e) => setGuardianPhone(e.target.value)}
                placeholder="017XXXXXXXX"
                className="w-full pl-9 pr-4 py-2.5 text-sm bg-white border border-slate-200 rounded-xl focus:border-blue-600 focus:ring-2 focus:ring-blue-100 outline-none text-slate-900 transition-all"
              />
            </div>
            <Button
              variant="brand"
              isLoading={isLoading}
              onClick={handleRequestConsent}
              className="h-10 px-5 text-sm font-semibold shrink-0"
            >
              Send Consent SMS
            </Button>
          </div>
          <p className="text-[11px] text-slate-400">
            We will dispatch a secure 1-click consent link via Bangla SMS valid for 24 hours.
          </p>
        </div>
      ) : (
        <div className="flex items-center justify-between p-4 rounded-xl bg-teal-50/50 border border-teal-100">
          <div className="flex items-center space-x-3">
            <UserCheck className="w-5 h-5 text-teal-600" />
            <div>
              <p className="text-xs font-semibold text-teal-900">Guardian Verified</p>
              <p className="text-xs text-teal-700 font-mono">{guardianPhone}</p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleRevokeConsent}
            className="text-xs text-rose-600 hover:text-rose-700 hover:bg-rose-50"
          >
            Revoke Consent
          </Button>
        </div>
      )}

      {/* Simulator / Demo link for testing */}
      {consentLink && status === 'PENDING' && (
        <div className="p-3.5 rounded-xl bg-blue-50/60 border border-blue-200 space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold text-blue-900">Guardian 1-Click Link Preview:</span>
            <button
              onClick={handleSimulateGuardianApproval}
              disabled={isLoading}
              className="font-semibold text-blue-700 hover:underline inline-flex items-center space-x-1"
            >
              <span>Simulate Guardian Approval</span>
              <ExternalLink className="w-3 h-3" />
            </button>
          </div>
          <p className="text-[11px] font-mono text-blue-800 break-all bg-white/80 p-2 rounded-lg border border-blue-100">
            {consentLink}
          </p>
        </div>
      )}

      {/* Feedback Messages */}
      {errorMessage && (
        <div className="flex items-center space-x-2 p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs font-medium">
          <AlertCircle className="w-4 h-4 shrink-0 text-rose-500" />
          <span>{errorMessage}</span>
        </div>
      )}

      {successMessage && (
        <div className="flex items-center space-x-2 p-3 rounded-lg bg-teal-50 border border-teal-200 text-teal-800 text-xs font-medium">
          <CheckCircle2 className="w-4 h-4 shrink-0 text-teal-600" />
          <span>{successMessage}</span>
        </div>
      )}
    </div>
  );
};
