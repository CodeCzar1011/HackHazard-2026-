import axios from "axios";
import type { LoginPayload, SignupPayload, AuthSession, TokenPairDto } from "@/types/api";

const TOKEN_KEY = "aegisflow.auth.session";
const API_KEY_KEY = "aegisflow.auth.api_key";
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  import.meta.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";

function mapAuthSession(tokenPair: TokenPairDto, apiKey?: string): AuthSession {
  return {
    accessToken: tokenPair.access_token,
    refreshToken: tokenPair.refresh_token,
    expiresAt: Date.now() + tokenPair.expires_in * 1000,
    role: tokenPair.user.role,
    user: {
      id: tokenPair.user.id,
      name: tokenPair.user.name,
      email: tokenPair.user.email,
    },
    apiKey,
  };
}

export const authService = {
  async login(payload: LoginPayload): Promise<AuthSession> {
    const apiKey = localStorage.getItem(API_KEY_KEY) ?? undefined;
    const { data } = await axios.post<TokenPairDto>(`${API_BASE_URL}/api/v1/auth/login`, {
      email: payload.email,
      password: payload.password,
    });
    const session = mapAuthSession(data, apiKey);
    localStorage.setItem(TOKEN_KEY, JSON.stringify(session));
    return session;
  },

  async signup(payload: SignupPayload): Promise<AuthSession> {
    // Backend currently provides admin-login flow; signup reuses login semantics.
    return this.login({ email: payload.email, password: payload.password, remember: true });
  },

  async logout(): Promise<void> {
    localStorage.removeItem(TOKEN_KEY);
  },

  async refresh(session: AuthSession | null): Promise<AuthSession | null> {
    if (!session) return null;
    if (session.expiresAt > Date.now() + 30_000) return session;
    const { data } = await axios.post<TokenPairDto>(`${API_BASE_URL}/api/v1/auth/refresh`, {
      refresh_token: session.refreshToken,
    });
    const next = mapAuthSession(data, session.apiKey);
    localStorage.setItem(TOKEN_KEY, JSON.stringify(next));
    return next;
  },

  getPersistedSession(): AuthSession | null {
    const raw = localStorage.getItem(TOKEN_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw) as AuthSession;
    } catch {
      return null;
    }
  },

  setApiKey(apiKey: string): void {
    localStorage.setItem(API_KEY_KEY, apiKey);
    const raw = localStorage.getItem(TOKEN_KEY);
    if (!raw) return;
    try {
      const session = JSON.parse(raw) as AuthSession;
      localStorage.setItem(TOKEN_KEY, JSON.stringify({ ...session, apiKey }));
    } catch {
      // Ignore invalid session cache.
    }
  },
};
