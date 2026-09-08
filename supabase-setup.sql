-- MAF MSP — msp_applications table
-- Run in Supabase Dashboard → SQL Editor → New Query
-- Project: zbjioabligamwmqgtxqs (MAF Product Page)
-- Columns match the POST payload in apply.html (see verify/check_payload_columns.py)

CREATE TABLE IF NOT EXISTS public.msp_applications (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  company TEXT NOT NULL,
  website TEXT,
  team_size TEXT,
  industry TEXT,
  revenue TEXT,
  owner TEXT,
  bottleneck TEXT,
  leaking_workflow TEXT,
  urgency TEXT,
  budget TEXT,
  tier TEXT,
  case_study TEXT,
  call_time TEXT,
  constraint_id TEXT
);

-- Enable RLS
ALTER TABLE public.msp_applications ENABLE ROW LEVEL SECURITY;

-- Allow anon inserts (the form uses the anon/publishable key — anon inserts are the point)
CREATE POLICY "allow_anon_insert" ON public.msp_applications
  FOR INSERT TO anon
  WITH CHECK (true);

-- No anon SELECT: applications stay private
CREATE POLICY "block_anon_select" ON public.msp_applications
  FOR SELECT TO anon
  USING (false);

CREATE POLICY "block_anon_update" ON public.msp_applications
  FOR UPDATE TO anon
  USING (false);

CREATE POLICY "block_anon_delete" ON public.msp_applications
  FOR DELETE TO anon
  USING (false);
