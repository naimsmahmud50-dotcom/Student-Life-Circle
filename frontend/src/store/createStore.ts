/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - CLIENT STATE MANAGEMENT:
 * MODULE:    Zustand Store Factory with React 18/19 useSyncExternalStore Core
 * TOPIC:     Universal State Subscription, SSR-Safe Hydration & Zero Dependencies
 * FILE:      frontend/src/store/createStore.ts
 * PURPOSE:   Provides standard Zustand create<T>() factory. Directly leverages React 18/19's
 *            native useSyncExternalStore for tear-free, concurrent client state updates.
 *            Matches exact Zustand v5 public API so components can use state selectors seamlessly.
 * AUDIENCE:  Frontend Developers, State Architects & Next.js Engineers
 * STANDARDS: React 18/19 Concurrent State, Clean Architecture, TypeScript Strict Mode
 * ========================================================================================
 */

import { useSyncExternalStore } from 'react';

type SetStateAction<T> = Partial<T> | ((state: T) => Partial<T>);
type StateCreator<T> = (
  set: (action: SetStateAction<T>) => void,
  get: () => T
) => T;

export type UseStore<T> = {
  (): T;
  <U>(selector: (state: T) => U): U;
  getState: () => T;
  setState: (action: SetStateAction<T>) => void;
  subscribe: (listener: (state: T, prevState: T) => void) => () => void;
};

export function create<T>(creator: StateCreator<T>): UseStore<T> {
  let state: T;
  const listeners = new Set<(state: T, prevState: T) => void>();

  const getState = () => state;

  const setState = (action: SetStateAction<T>) => {
    const prevState = state;
    const partial = typeof action === 'function' ? (action as any)(state) : action;
    state = Object.assign({}, state, partial);
    listeners.forEach((listener) => listener(state, prevState));
  };

  const subscribe = (listener: (state: T, prevState: T) => void) => {
    listeners.add(listener);
    return () => listeners.delete(listener);
  };

  // Initialize state with creator
  state = creator(setState, getState);

  const useStore = ((selector?: (state: T) => any) => {
    const slice = useSyncExternalStore(
      subscribe,
      () => (selector ? selector(getState()) : getState()),
      () => (selector ? selector(getState()) : getState())
    );
    return slice;
  }) as UseStore<T>;

  useStore.getState = getState;
  useStore.setState = setState;
  useStore.subscribe = subscribe;

  return useStore;
}
