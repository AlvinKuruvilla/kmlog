import { createClient } from "@supabase/supabase-js";

/* ------------------------------------------------------------------ */
/* 1. Supabase client                                                 */
/* ------------------------------------------------------------------ */
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_KEY
);

/* ------------------------------------------------------------------ */
/* 2.  CORS helpers                                                   */
/* ------------------------------------------------------------------ */
const ALLOW_ORIGIN = "https://fakeprofiledetection.github.io"; // change / add as needed

const corsHeaders = {
  "Access-Control-Allow-Origin": ALLOW_ORIGIN, // echo the GitHub‑Pages origin
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Access-Control-Max-Age": "86400", // cache preflight 24 h
};

/* ------------------------------------------------------------------ */
/* 3.  Function handler                                               */
/* ------------------------------------------------------------------ */
export const handler = async (event) => {
  const { httpMethod } = event;

  /* ---- 3.1  CORS pre‑flight -------------------------------------- */
  if (httpMethod === "OPTIONS") {
    return { statusCode: 200, headers: corsHeaders, body: "" };
  }

  /* ---- 3.2  block everything but POST ---------------------------- */
  if (httpMethod !== "POST") {
    return {
      statusCode: 405,
      headers: corsHeaders,
      body: "Only POST allowed",
    };
  }

  try {
    /* ---- 3.3  extract file from multipart/form‑data -------------- */
    const contentType =
      event.headers["content-type"] || event.headers["Content-Type"] || "";
    const boundary = contentType.split("boundary=")[1];
    if (!boundary) throw new Error("Missing multipart boundary");

    const body = Buffer.from(event.body, "base64");
    const parts = body.toString().split(`--${boundary}`);
    const filePart = parts.find(
      (p) => p.includes("Content-Disposition") && p.includes("filename=")
    );
    if (!filePart) throw new Error("No file part found");

    const [, fileName = `upload-${Date.now()}`] =
      filePart.match(/filename="(.+?)"/) || [];

    const fileData = filePart.split("\r\n\r\n")[1].split("\r\n")[0];
    const fileBuffer = Buffer.from(fileData, "binary");

    /* ---- 3.4  upload to Supabase Storage ------------------------- */
    const { error } = await supabase.storage
      .from("data-collection-files")
      .upload(`uploads/${fileName}`, fileBuffer, { upsert: true });

    if (error) throw error;

    /* ---- 3.5  public URL to return ------------------------------- */
    const url = `${process.env.SUPABASE_URL}/storage/v1/object/public/data-collection-files/uploads/${fileName}`;

    return {
      statusCode: 200,
      headers: corsHeaders,
      body: JSON.stringify({ url }),
    };
  } catch (err) {
    console.error("Saver error:", err);
    return {
      statusCode: 500,
      headers: corsHeaders, // ← still include CORS so client can read it
      body: JSON.stringify({ error: err.message || err }),
    };
  }
};
