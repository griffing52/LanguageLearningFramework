export async function GET(
  _: Request,
  context: { params: Promise<{ planId: string }> },
) {
  const { planId } = await context.params;
  const payload = {
    planId,
    message:
      "Mock stream endpoint. Replace this route with provider-backed audio file streaming.",
  };

  return new Response(JSON.stringify(payload), {
    headers: {
      "content-type": "application/json",
      "cache-control": "no-store",
    },
    status: 200,
  });
}
