/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic 3D WebGL Error Boundary
 * FILE:      frontend/src/components/3d/Academic3DErrorBoundary.tsx
 * PURPOSE:   Catches any WebGL context errors, canvas crashes, or chunk loading failures:
 *            - Replaces crashed canvas seamlessly with the pristine 2D fallback graphic.
 *            - Zero layout shift (CLS = 0).
 *            - Automatically reports fallback state to capability layer without alerting the user.
 * STANDARDS: Strict Zero-Emoji, Production Grade Resilience, Zero Unhandled Exceptions.
 */

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AcademicPristine2DFallback } from './AcademicPristine2DFallback';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  size?: number;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class Academic3DErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.warn('[Ogrojatra 3D Boundary] WebGL runtime error caught, rendering 2D fallback:', error);
    this.props.onError?.(error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <AcademicPristine2DFallback size={this.props.size || 280} />
        )
      );
    }

    return this.props.children;
  }
}
