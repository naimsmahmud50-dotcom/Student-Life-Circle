/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Role-Based Access Control (RBAC) & Identity Types
 * TOPIC:     Platform Role Enums, Permissions Matrix & Session Contracts
 * FILE:      frontend/src/lib/auth-types.ts
 * PURPOSE:   Provides a single source of truth for user roles, access level
 *            hierarchies, and session type contracts across all client-side guards
 *            and admin consoles. Mirrors backend.app.models.user.UserRoleEnum.
 * STANDARDS: Strict TypeScript, Zero-Emoji, Zero-Trust Architecture
 */

export enum UserRole {
  STUDENT = 'STUDENT',
  GUARDIAN = 'GUARDIAN',
  TUTOR = 'TUTOR',
  EMPLOYER = 'EMPLOYER',
  CONTENT_EDITOR = 'CONTENT_EDITOR',
  SUBJECT_REVIEWER = 'SUBJECT_REVIEWER',
  SAFETY_MODERATOR = 'SAFETY_MODERATOR',
  ADMIN = 'ADMIN',
}

/**
 * Roles permitted to enter the /admin area.
 * - ADMIN: Full administrative authority across all modules, arbitration, and telemetry.
 * - SUBJECT_REVIEWER: Scoped authority restricted to question quarantine & content review queues.
 */
export const ADMIN_PANEL_ROLES: readonly UserRole[] = [
  UserRole.ADMIN,
  UserRole.SUBJECT_REVIEWER,
] as const;

/**
 * Roles permitted to perform system-level management (escrow release, key rotation, node config).
 */
export const FULL_ADMIN_ROLES: readonly UserRole[] = [
  UserRole.ADMIN,
] as const;

/**
 * Roles permitted to review content and trigger question quarantine.
 */
export const CONTENT_REVIEW_ROLES: readonly UserRole[] = [
  UserRole.ADMIN,
  UserRole.SUBJECT_REVIEWER,
  UserRole.CONTENT_EDITOR,
] as const;

export interface AuthenticatedUser {
  id: string;
  email?: string | null;
  phone?: string | null;
  fullName: string;
  roles: UserRole[];
  avatarUrl?: string | null;
  isPhoneVerified?: boolean;
  isEmailVerified?: boolean;
}

export interface AuthSession {
  user: AuthenticatedUser;
  token: string;
  issuedAt: number; // Unix timestamp in milliseconds
  expiresAt: number; // Unix timestamp in milliseconds (e.g. 7 days or 24 hours)
}

/**
 * Evaluates whether a set of user roles satisfies any of the required roles.
 */
export function hasAnyRole(
  userRoles: readonly (UserRole | string)[] | undefined | null,
  requiredRoles: readonly UserRole[]
): boolean {
  if (!userRoles || userRoles.length === 0) return false;
  const normalized = new Set(userRoles.map((r) => r.toUpperCase()));
  return requiredRoles.some((req) => normalized.has(req));
}

/**
 * Checks whether user has full administrator privileges.
 */
export function isFullAdmin(userRoles?: readonly (UserRole | string)[] | null): boolean {
  return hasAnyRole(userRoles, FULL_ADMIN_ROLES);
}

/**
 * Checks whether user has subject reviewer privileges.
 */
export function isSubjectReviewer(userRoles?: readonly (UserRole | string)[] | null): boolean {
  return hasAnyRole(userRoles, [UserRole.SUBJECT_REVIEWER]);
}

/**
 * Checks whether user can enter the admin console.
 */
export function canAccessAdminPanel(userRoles?: readonly (UserRole | string)[] | null): boolean {
  return hasAnyRole(userRoles, ADMIN_PANEL_ROLES);
}

/**
 * Checks whether user can execute question quarantine actions.
 */
export function canQuarantineQuestions(userRoles?: readonly (UserRole | string)[] | null): boolean {
  return hasAnyRole(userRoles, CONTENT_REVIEW_ROLES);
}
