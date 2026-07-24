const TOKEN_KEY = "sgs_access_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export type CurrentUser = {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
};

export async function login(email: string, password: string): Promise<string> {
  const body = new URLSearchParams();
  body.set("username", email);
  body.set("password", password);

  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  if (!res.ok) {
    throw new Error("E-Mail oder Passwort ist falsch");
  }

  const data = await res.json();
  return data.access_token as string;
}

export async function fetchCurrentUser(token: string): Promise<CurrentUser> {
  const res = await fetch("/api/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    throw new Error("Sitzung abgelaufen");
  }

  return res.json();
}
