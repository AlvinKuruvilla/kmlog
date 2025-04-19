import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

export const handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Only POST allowed" };
  }
  /* ---------- CORS pre‑flight ---------- */
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      },
      body: "",
    };
  }

  const contentType =
    event.headers["content-type"] || event.headers["Content-Type"];
  const boundary = contentType.split("boundary=")[1];
  const body = Buffer.from(event.body, "base64");
  const parts = body.toString().split(`--${boundary}`);

  const filePart = parts.find(
    (p) => p.includes("Content-Disposition") && p.includes("filename=")
  );
  const [, fileName = `upload-${Date.now()}`] =
    filePart.match(/filename="(.+?)"/) || [];

  const fileData = filePart.split("\r\n\r\n")[1].split("\r\n")[0];
  const fileBuffer = Buffer.from(fileData, "binary");

  const { error } = await supabase.storage
    .from("data-collection-files")
    .upload(`uploads/${fileName}`, fileBuffer, { upsert: true });

  if (error) {
    return { statusCode: 500, body: JSON.stringify({ error }) };
  }

  const url = `${process.env.SUPABASE_URL}/storage/v1/object/public/data-collection-files/uploads/${fileName}`;
  return { statusCode: 200, body: JSON.stringify({ url }) };
};
