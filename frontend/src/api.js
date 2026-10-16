export async function request(path = '', options = {}) {
  const response = await fetch(`/api/tickets${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options.headers },
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(typeof payload.detail === 'string' ? payload.detail : `Request failed (${response.status}). Check the ticket fields and try again.`);
  }
  return response.status === 204 ? null : response.json();
}
