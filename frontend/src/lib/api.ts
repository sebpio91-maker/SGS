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

async function authFetch(path: string, options: RequestInit = {}): Promise<Response> {
  const token = getToken();
  const headers = new Headers(options.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (options.body) headers.set("Content-Type", "application/json");

  const res = await fetch(`/api${path}`, { ...options, headers });
  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const data = await res.json();
      detail = data.detail ?? detail;
    } catch {
      /* Antwort ohne JSON-Body (z.B. 204) */
    }
    throw new Error(detail);
  }
  return res;
}

export type Customer = {
  id: number;
  name: string;
  code: string;
  notes: string | null;
};

export type CustomerInput = {
  name: string;
  code: string;
  notes?: string | null;
};

export async function listCustomers(): Promise<Customer[]> {
  return (await authFetch("/customers")).json();
}

export async function createCustomer(input: CustomerInput): Promise<Customer> {
  return (await authFetch("/customers", { method: "POST", body: JSON.stringify(input) })).json();
}

export async function updateCustomer(
  id: number,
  input: Partial<CustomerInput>,
): Promise<Customer> {
  return (
    await authFetch(`/customers/${id}`, { method: "PATCH", body: JSON.stringify(input) })
  ).json();
}

export async function deleteCustomer(id: number): Promise<void> {
  await authFetch(`/customers/${id}`, { method: "DELETE" });
}

export type Product = {
  id: number;
  customer_id: number;
  article_number: string;
  name: string;
  category: string | null;
  has_battery: boolean;
  has_manual: boolean;
  specification: Record<string, unknown> | null;
};

export type ProductInput = {
  customer_id: number;
  article_number: string;
  name: string;
  category?: string | null;
  has_battery?: boolean;
  has_manual?: boolean;
  specification?: Record<string, unknown> | null;
};

export async function listProducts(customerId?: number): Promise<Product[]> {
  const query = customerId ? `?customer_id=${customerId}` : "";
  return (await authFetch(`/products${query}`)).json();
}

export async function createProduct(input: ProductInput): Promise<Product> {
  return (await authFetch("/products", { method: "POST", body: JSON.stringify(input) })).json();
}

export async function updateProduct(
  id: number,
  input: Partial<ProductInput>,
): Promise<Product> {
  return (
    await authFetch(`/products/${id}`, { method: "PATCH", body: JSON.stringify(input) })
  ).json();
}

export async function deleteProduct(id: number): Promise<void> {
  await authFetch(`/products/${id}`, { method: "DELETE" });
}
