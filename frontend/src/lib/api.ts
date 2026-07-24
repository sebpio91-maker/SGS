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
  // FormData setzt seinen eigenen multipart-Content-Type inkl. Boundary;
  // den nicht überschreiben.
  if (options.body && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

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
  kategorie?: string | null;
  produktart?: string | null;
  zielgruppe?: string | null;
  einsatzort?: string | null;
  bereich?: string | null;
  produkt_typ?: string | null;
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

export type TestOrder = {
  id: number;
  customer_id: number;
  product_id: number | null;
  order_number: string | null;
  source: string;
  original_filename: string | null;
  status: string;
  raw_data: Record<string, unknown> | null;
};

export type LidlImportResult = {
  product: Product;
  test_order: TestOrder;
  pruefumfang_kategorien: string[];
  referenzpruefung: boolean;
  ngo_pruefung: boolean;
  ffu_pruefung: boolean;
};

export async function importLidlPruefauftrag(file: File): Promise<LidlImportResult> {
  const formData = new FormData();
  formData.append("file", file);
  return (
    await authFetch("/test-orders/import-lidl", { method: "POST", body: formData })
  ).json();
}

export async function listTestOrders(customerId?: number): Promise<TestOrder[]> {
  const query = customerId ? `?customer_id=${customerId}` : "";
  return (await authFetch(`/test-orders${query}`)).json();
}

export type TestPlanItem = {
  id: number;
  catalog_item_id: number | null;
  category_name: string;
  name: string;
  norm_reference: string | null;
  description: string | null;
  result: string | null;
  remarks: string | null;
  lab_minutes: number | null;
  lab_cost: number | null;
  sale_price: number | null;
  sort_order: number;
};

export type TestPlan = {
  id: number;
  customer_id: number;
  product_id: number;
  test_order_id: number | null;
  status: string;
  items: TestPlanItem[];
  lab_minutes_total: number;
  lab_cost_total: number;
  sale_price_total: number;
};

export type GenerateTestPlanInput = {
  product_id: number;
  test_order_id?: number | null;
  selected_catalog_item_ids?: number[];
  selected_spec_requirement_ids?: number[];
  selected_special_item_eigenschaften?: string[];
};

export async function generateTestPlan(input: GenerateTestPlanInput): Promise<TestPlan> {
  return (
    await authFetch("/test-plans/generate", { method: "POST", body: JSON.stringify(input) })
  ).json();
}

export async function listTestPlans(productId?: number): Promise<TestPlan[]> {
  const query = productId ? `?product_id=${productId}` : "";
  return (await authFetch(`/test-plans${query}`)).json();
}
