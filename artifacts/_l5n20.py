# _l5n20.py -- NULL-TIGHTENING RE-DRAW of the L5 +/-3sigma matched-random null at N=20.
# PROPOSE-ONLY. GPT-2 124M. NOT a new claim: replaces the L5 N=3 null DISCLOSURE (paper 6.6).
# Pre-registration: FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md ::
#   "L5N20 -- NULL-TIGHTENING RE-DRAW OF THE L5 +/-3sigma MATCHED-RANDOM NULL AT N=20 --
#    GAP + PRE-REGISTRATION (2026-07-06 ~19:03)".
# Brief: PATCH_BRIEF_2026-07-06.md STEP 2 (Will: "do all three").
# MACHINERY BYTE-VERBATIM from _l6.py (d7ab446ba5aacaa5): model loader / capture_h_all /
#   InjectHook / rep_feats / RUNG onset_b6 / rung_edit_delta / onset_perpos / onset_mean /
#   onset_null / pct95. This script changes ONLY which null draws are taken (M3 replay stream +
#   M4 fresh SEED_N20 stream) -- never the instruments. No weights trained. Zero DB writes.
import json, time, os, math, traceback, gc, subprocess, hashlib, ctypes
import torch, torch.nn as nn, torch.nn.functional as Fnn

t0=time.time()
DIR=r"C:\Shadow\Dissector\D0_PROGRAM\CONSTRUCTIVE"
SMOKE=os.environ.get("L5N20_SMOKE")=="1"
LOG=open(os.path.join(DIR,"_l5n20.log"),"a",encoding="utf-8")
def logln(s):
    s=str(s); LOG.write(f"[L5N20 {round(time.time()-t0,1):8.1f}s] "+s+"\n"); LOG.flush()
    try: print(s,flush=True)
    except Exception: pass
def el(): return round(time.time()-t0,1)
logln("="*100); logln(f"L5N20 START smoke={SMOKE} torch={torch.__version__}")
try:
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(),0x4000)
    logln("[ops] priority BelowNormal set")
except Exception as e: logln(f"[ops] priority set failed: {e}")
torch.set_num_threads(6)

# ---------------- locked constants (pre-reg verbatim; L6 header verbatim) ----------------
EPS_KL=0.1871; CERT_BLOCK=512; IND_SEG=64; MB=4; CAP_CHUNK=16
VOCAB_SANS_SPECIALS=50256
FRESH_LO,FRESH_HI=24576,32768; REP_SEED=3
N_HOLD=16; TOL_REPLAY=2e-3; TOL_MAG=1e-2
DEC_V7_SHA="b1d2f464c00c3ef6"; ENC_SHA="6be189567c41e91d"; ENCJ_SHA="365dc3ff592fc6bd"
FREC_SHA="71549ae3afcc8d07"; LEX_SHA="71a51619a9bb25c3"; GRAM_SHA="da6f8a63a061782b"
MAPS_SHA="b43f877af68728df"; WP_SHA="ea5236cbd608a385"; OS_SHA="77dd0948a63bb24f"
SEED_OQ4=20260707+29         # L6 OQ-4 generator (replay stream; mag6 draws consumed first)
SEED_N20=20260708+37         # FRESH re-draw seed (pre-reg; never used by any prior stage)
N_NULL=1 if SMOKE else 20
N_DISCARD=20                 # the L6 mag6 stream consumed exactly 20 randn(d) draws first
# banked deterministic anchors (byte-replay gates; L5/_l5_result.json + L6/_l6_result.json)
GB1_AON=-0.00388             # rung +/-3 behavioral antisym (L5)
GB1_MAG3=7.8544              # rung mag3 (L5)
GB2_MCLEAN=0.9569            # clean M_onset (L5 0.95686, pen anchor 0.9569)
L6_NULL95_20_MAG3=0.00289    # L6 report-only re-arm null95_20_mag3 (the M3 replay target)
L5_NULL95_N3=0.00993         # L5 verdict null at N=3 (the disclosure this run replaces)
TOL_NULLREPLAY=5e-5
SOFT_WALL_S=25*60; HARD_WALL_S=30*60

RESULT_JSON=os.path.join(DIR,"_l5n20_result_SMOKE.json" if SMOKE else "_l5n20_result.json")
torch.manual_seed(1234)

PEN=("FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md :: 'L5N20 -- NULL-TIGHTENING RE-DRAW OF THE L5 "
     "+/-3sigma MATCHED-RANDOM NULL AT N=20 -- GAP + PRE-REGISTRATION (2026-07-06 ~19:03)'")
res={"experiment":"L5N20 null-tightening re-draw: the L5 Arm-B +/-3sigma matched-random-edit null "
     "re-drawn at honest N=20 (byte-verbatim L6/L5 rung machinery; M3 replay of L6's "
     "null95_20_mag3 first, then M4 fresh SEED_N20 draw). NOT a new claim -- replaces the N=3 "
     "null disclosure. GPT-2 124M.",
     "date":"2026-07-06","propose_only":True,"pre_registration":PEN,
     "locked":{"tol_replay":TOL_REPLAY,"tol_mag":TOL_MAG,"tol_nullreplay":TOL_NULLREPLAY,
        "n_null":N_NULL,"n_discard":N_DISCARD,"seed_oq4":SEED_OQ4,"seed_n20":SEED_N20,
        "banked":{"GB1_AON":GB1_AON,"GB1_MAG3":GB1_MAG3,"L6_NULL95_20_MAG3":L6_NULL95_20_MAG3,
                  "L5_NULL95_N3":L5_NULL95_N3},
        "bands":"R=|A_on|/null95_20_new: BEATS R>1.1 / KNIFE-EDGE 0.9<=R<=1.1 / BELOW R<0.9 ; "
                "bet BEATS65/KNIFE20/BELOW15 ; verdicts untouched in every branch"},
     "config":{"n_hold":N_HOLD,"mb":MB,"cap_chunk":CAP_CHUNK,"cert_block":CERT_BLOCK,
        "ind_seg":IND_SEG,"precision":"fp32","tf32":"off","attn":"eager","seed":1234,"smoke":SMOKE},
     "gpu_free_checks":[],"instrument_discrepancy":[],"gates":{},"m3_replay":{},"m4_fresh":{},
     "verdict":{},"status":"INIT"}

def write_json():
    res["elapsed_s"]=el(); tmp=RESULT_JSON+".tmp"
    with open(tmp,"w",encoding="utf-8") as f: json.dump(res,f,indent=1,default=str)
    os.replace(tmp,RESULT_JSON)

# ---------------- resume ----------------
if os.path.exists(RESULT_JSON):
    try:
        prev=json.load(open(RESULT_JSON,encoding="utf-8"))
        for k in ("gates","m3_replay","m4_fresh","verdict","gpu_free_checks","instrument_discrepancy"):
            if prev.get(k): res[k]=prev[k]
        logln(f"*** RESUME *** gates={list(res['gates'].keys())} m3={list(res['m3_replay'].keys())} m4={list(res['m4_fresh'].keys())}")
    except Exception as e: logln(f"resume load fail {e}")

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for ch in iter(lambda:f.read(1<<20),b""): h.update(ch)
    return h.hexdigest()[:16]
def gpu_free_check(tag):
    rec={"tag":tag,"t":el(),"foreign":[]}
    try:
        out=subprocess.run(["nvidia-smi","--query-compute-apps=pid,process_name,used_memory","--format=csv,noheader"],
                           capture_output=True,text=True,timeout=30).stdout
        me=os.getpid()
        for line in out.strip().splitlines():
            p=[x.strip() for x in line.split(",")]
            if len(p)>=3 and p[0].isdigit() and int(p[0])!=me and "python" in p[1].lower(): rec["foreign"].append(line)
    except Exception as e: rec["error"]=str(e)
    waited=0
    while rec["foreign"] and waited<600:
        logln(f"[gpu {tag}] FOREIGN {rec['foreign']} wait60"); time.sleep(60); waited+=60
        try:
            out=subprocess.run(["nvidia-smi","--query-compute-apps=pid,process_name,used_memory","--format=csv,noheader"],
                               capture_output=True,text=True,timeout=30).stdout
            me=os.getpid(); rec["foreign"]=[]
            for line in out.strip().splitlines():
                p=[x.strip() for x in line.split(",")]
                if len(p)>=3 and p[0].isdigit() and int(p[0])!=me and "python" in p[1].lower(): rec["foreign"].append(line)
        except Exception: break
    rec["waited_s"]=waited; rec["clear"]=not rec["foreign"]
    if rec["foreign"]: res["instrument_discrepancy"].append({"stage":tag,"name":"gpu_free_check","why":str(rec["foreign"])})
    res["gpu_free_checks"].append(rec); write_json(); logln(f"[gpu {tag}] clear={rec['clear']}"); return rec["clear"]
def free(): gc.collect(); torch.cuda.empty_cache()
def pct95(xs):
    xs=sorted(xs); return xs[min(len(xs)-1,int(math.ceil(0.95*len(xs))-1))] if xs else 0.0
def flag(stage,name,why):
    res["instrument_discrepancy"].append({"stage":stage,"name":name,"why":str(why)}); write_json()
    logln(f"[FB {stage}] {name}: {why}")

# ---------------- model (v7/l4/l5/l6 loader verbatim) ----------------
from transformers import AutoModelForCausalLM, AutoTokenizer
M={"m":None}
def ensure_model():
    if M["m"] is not None: return
    if not torch.cuda.is_available(): raise RuntimeError("CUDA not available")
    torch.backends.cuda.matmul.allow_tf32=False; torch.backends.cudnn.allow_tf32=False
    tok=AutoTokenizer.from_pretrained("gpt2")
    model=AutoModelForCausalLM.from_pretrained("gpt2",dtype=torch.float32,attn_implementation="eager").to('cuda').eval()
    model.requires_grad_(False)
    M["m"]=model; M["tok"]=tok; M["blocks"]=list(model.transformer.h); M["drop"]=model.transformer.drop
    M["d"]=model.config.n_embd; M["nL"]=model.config.n_layer
    M["wte"]=model.transformer.wte.weight.detach().float()
    M["lnf"]=model.transformer.ln_f.weight.detach().float()
    res["gpt2_meta"]={"n_layer":M["nL"],"d":M["d"],"precision":"fp32","tf32":"off","attn":"eager"}
    logln(f"[gpt2] loaded fp32 eager nL={M['nL']} d={M['d']}")

def build_dind(n_blocks,block,seed):
    g=torch.Generator().manual_seed(seed)
    seg=torch.randint(0,VOCAB_SANS_SPECIALS,(n_blocks,IND_SEG),generator=g)
    return seg.repeat(1,block//IND_SEG)

# ---------------- KL kernel + inject (v7/l4/l5/l6 verbatim) ----------------
def fkl(yt,yp):
    logp=Fnn.log_softmax(yt,-1); p=logp.exp(); lp=Fnn.log_softmax(yp,-1)
    return (p*(logp-lp)).sum(-1)
class InjectHook:
    def __init__(self,block):
        self.on=False; self.add=None; self.handle=block.register_forward_hook(self._h)
    def _h(self,mod,inp,out):
        if not self.on: return None
        hs=out[0] if isinstance(out,tuple) else out
        hs2=hs+self.add
        if isinstance(out,tuple): return (hs2,)+tuple(out[1:])
        return hs2
    def close(self): self.handle.remove()
def clean_logits(ids_cpu):
    model=M["m"]; N=ids_cpu.shape[0]; outs=[]
    with torch.no_grad():
        for s0 in range(0,N,MB):
            s1=min(N,s0+MB); lg=model(ids_cpu[s0:s1].to('cuda'),use_cache=False).logits.detach(); outs.append(lg)
    return outs
def inject_kl_full(ids_cpu,injhook,delta_full_g,Yclean,want_dl=False):
    model=M["m"]; N=ids_cpu.shape[0]; tot=0.0; cnt=0; ci=0; dlmax=0.0
    with torch.no_grad():
        for s0 in range(0,N,MB):
            s1=min(N,s0+MB)
            injhook.add=delta_full_g[s0:s1].to('cuda').float(); injhook.on=True
            lg=model(ids_cpu[s0:s1].to('cuda'),use_cache=False).logits; injhook.on=False; injhook.add=None
            kl=fkl(Yclean[ci].float(),lg.float()); tot+=kl.sum().item(); cnt+=kl.numel()
            if want_dl: dlmax=max(dlmax,float((lg.float()-Yclean[ci].float()).abs().max()))
            ci+=1; del lg
    m=tot/max(1,cnt)
    return (m,dlmax) if want_dl else m
def capture_h_all(ids_cpu,tag,extra_wm0=False):
    model=M["m"]; nL=M["nL"]; N=ids_cpu.shape[0]; d=M["d"]; buf={}
    def mk(key):
        def h(mod,inp,out): buf[key]=(out[0] if isinstance(out,tuple) else out).detach()
        return h
    hh=[M["drop"].register_forward_hook(mk(0))]
    for L in range(nL): hh.append(M["blocks"][L].register_forward_hook(mk(L+1)))
    if extra_wm0: hh.append(M["blocks"][0].mlp.register_forward_hook(lambda m,i,o: buf.__setitem__('wm0',o.detach())))
    acc={b:[] for b in range(nL+1)}
    if extra_wm0: acc['wm0']=[]
    with torch.no_grad():
        for c0 in range(0,N,CAP_CHUNK):
            c1=min(N,c0+CAP_CHUNK); _=model(ids_cpu[c0:c1].to('cuda'),use_cache=False)
            for b in range(nL+1): acc[b].append(buf[b].reshape(-1,d).cpu())
            if extra_wm0: acc['wm0'].append(buf['wm0'].reshape(-1,d).cpu())
    for x in hh: x.remove()
    out={b:torch.cat(acc[b]) for b in range(nL+1)}
    if extra_wm0: out['wm0']=torch.cat(acc['wm0'])
    logln(f"[capture {tag}] N={N} boundaries={nL+1} extra_wm0={extra_wm0}")
    return out
class LinearRung(nn.Module):
    def __init__(self,fin,d): super().__init__(); self.w=nn.Linear(fin,d)
    def forward(self,x): return self.w(x)

# ======================================================================================
# MAIN
# ======================================================================================
try:
    ensure_model()
    d=M["d"]; nL=M["nL"]; tok=M["tok"]; wte_g=M["wte"]

    # ---- M1 GATE-0: hashes (ALL 8 locked; FB-A on any breach) ----
    if not res["gates"].get("hashes"):
        hh_={"encoder_v1":(sha256(os.path.join(DIR,"_l3_encoder.pt")),ENC_SHA),
             "encoder_json":(sha256(os.path.join(DIR,"ENCODER_V1.json")),ENCJ_SHA),
             "decoder_v7":(sha256(os.path.join(DIR,"decoder_v7_tensors.pt")),DEC_V7_SHA),
             "floors_recal":(sha256(os.path.join(DIR,"_v5_floors_recal.json")),FREC_SHA),
             "lexicon_v3":(sha256(os.path.join(DIR,"LEXICON_V3.md")),LEX_SHA),
             "grammar":(sha256(os.path.join(DIR,"GRAMMAR_TABLE_V1.json")),GRAM_SHA),
             "l2babel_maps":(sha256(os.path.join(DIR,"_l2babel_maps.pt")),MAPS_SHA),
             "wellposedness":(sha256(os.path.join(DIR,"WELLPOSEDNESS_TABLE_V1.json")),WP_SHA),
             "offspan":(sha256(os.path.join(DIR,"OFFSPAN_TABLE_V1.json")),OS_SHA)}
        hashrec={k:{"sha":v[0],"locked":v[1],"ok":bool(v[0]==v[1])} for k,v in hh_.items()}
        all_hash_ok=all(r["ok"] for r in hashrec.values())
        res["gates"]["hashes"]={"detail":hashrec,"pass":bool(all_hash_ok)}
        logln(f"[GATE-0] hashes ok={all_hash_ok} "+" ".join(f"{k}:{r['ok']}" for k,r in hashrec.items()))
        write_json()
        if not all_hash_ok and not SMOKE:
            res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-A: locked hash mismatch")

    # ---- load decoder_v7 + ENCODER_V1 (verbatim l4/l5/l6) ----
    D7=torch.load(os.path.join(DIR,"decoder_v7_tensors.pt"),map_location="cpu",weights_only=False)
    C=D7["C"].float(); B2=D7["B2"].float(); Q35=D7["Q35"].float(); Qu=D7["Q_union"].float()
    mu=D7["mu"].float(); read_W=D7["read_W"].float(); Vk=D7["m0_repera_Vk_recal"].float()
    ENC=torch.load(os.path.join(DIR,"_l3_encoder.pt"),map_location="cpu",weights_only=False)
    xcheck={}
    for nm,a,b in [("C",ENC["C"],C),("B2",ENC["B2"],B2),("Q35",ENC["Q35"],Q35),("Q_union",ENC["Q_union"],Qu),
                   ("mu",ENC["mu"],mu),("read_W",ENC["read_W"],read_W)]:
        xcheck[nm]=float((a.float()-b.float()).abs().max())
    enc_matches=all(v<=1e-6 for v in xcheck.values())
    res["gates"]["encoder_is_decoder_inverse"]={"max_abs_diff":xcheck,"pass":bool(enc_matches)}
    logln(f"[GATE-0b] ENCODER_V1==decoder_v7 reader: {xcheck} -> {enc_matches}")
    if not enc_matches and not SMOKE:
        res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-A: encoder not decoder inverse")
    B2_g=B2.to('cuda'); Q35_g=Q35.to('cuda'); span5=torch.cat([B2_g,Q35_g],1)
    Vk_g=Vk.to('cuda'); mu_g={b:mu[b].to('cuda') for b in range(nL+1)}
    def load_rung(sd_key,scm_key,scs_key):
        r=LinearRung(1537,d).to('cuda').eval()
        r.load_state_dict({k:v.to('cuda').float() for k,v in D7[sd_key].items()})
        return r, D7[scm_key].to('cuda').float(), D7[scs_key].to('cuda').float()
    RUNG={}
    RUNG[("repetition",6)]=load_rung("onset_b6_state_dict","onset_b6_scaler_mean","onset_b6_scaler_std")
    frec=json.load(open(os.path.join(DIR,"_v5_floors_recal.json"),encoding="utf-8"))
    RECAL_OK=(not frec.get("quarantined")) and frec.get("sg_early_ok") and frec.get("repl_all")
    res["gates"]["recal_ok"]=bool(RECAL_OK)
    logln(f"[objects] loaded. RECAL_OK={RECAL_OK}")
    if not RECAL_OK and not SMOKE:
        res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-A: RECAL not OK")

    def proj_compl(x): return x-(x@span5)@span5.t()

    # regime holdout stream (repetition only -- the only regime this stage forwards)
    gpu_free_check("setup")
    idsR=build_dind(N_HOLD,CERT_BLOCK,REP_SEED); N_R=idsR.shape[0]
    capR=capture_h_all(idsR,"reg-repetition",extra_wm0=True)
    YclR=clean_logits(idsR)

    # ---- M1b GATE-0 identity-inject exact-zero (repetition, matched batch shape MB) ----
    if not res["gates"].get("identity_inject"):
        inj0=InjectHook(M["blocks"][5])
        idkl,iddl=inject_kl_full(idsR,inj0,torch.zeros(N_R,CERT_BLOCK,d),YclR,want_dl=True); inj0.close()
        ok=bool(idkl<=1e-9 and iddl<=1e-4)
        res["gates"]["identity_inject"]={"detail":{"repetition":{"kl":idkl,"dlogit":round(iddl,7),"pass":ok}},
                                         "pass":bool(ok)}
        logln(f"[GATE-0 identity repetition] kl={idkl} dlogit={iddl} -> {ok}"); write_json()
        if not ok and not SMOKE:
            res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-A: identity-inject not exact-zero")

    # ---- Arm B setup (rung machinery byte-verbatim L6/L5) ----
    bb=6; rg="repetition"
    injR=InjectHook(M["blocks"][bb-1])
    def rep_feats(ids,cap):
        x2=cap[2].to('cuda')-mu_g[2]; ecur=wte_g[ids.reshape(-1).to('cuda')]; s=cap['wm0'].to('cuda')@Vk_g
        return x2,ecur,s
    x2R,ecurR,sR=rep_feats(idsR,capR); featsR=torch.cat([x2R,ecurR,sR],1)
    rung,scm,scs=RUNG[(rg,bb)]
    with torch.no_grad(): oh_real=proj_compl(rung((featsR-scm)/scs))
    sig_s=float(sR.std())
    def rung_edit_delta(k):
        s2=sR+k*sig_s; feats2=torch.cat([x2R,ecurR,s2],1)
        with torch.no_grad(): ohp=proj_compl(rung((feats2-scm)/scs))
        dv=(ohp-oh_real).reshape(N_R,CERT_BLOCK,d).contiguous(); dv=dv.clone(); dv[:, :IND_SEG, :]=0.0
        mag=float(dv[:, IND_SEG:, :].reshape(-1,d).norm(dim=1).mean())
        return dv,mag
    def onset_perpos(injhook,delta_full_g):
        model=M["m"]; out=[]
        with torch.no_grad():
            for s0 in range(0,N_R,MB):
                s1=min(N_R,s0+MB)
                if injhook is not None: injhook.add=delta_full_g[s0:s1].to('cuda').float(); injhook.on=True
                lg=model(idsR[s0:s1].to('cuda'),use_cache=False).logits.float()
                if injhook is not None: injhook.on=False; injhook.add=None
                lp=Fnn.log_softmax(lg,-1)
                tgt=idsR[s0:s1,1:].to('cuda')
                sl=lp[:,IND_SEG:CERT_BLOCK-1,:].gather(-1,tgt[:,IND_SEG:CERT_BLOCK-1].unsqueeze(-1)).squeeze(-1).exp()
                out.append(sl.cpu()); del lg,lp
        return torch.cat(out)
    def onset_mean(injhook,delta_full_g): return float(onset_perpos(injhook,delta_full_g).mean())

    # ---- M2 GB-1 REPLAY GATE: rung +/-3 behavioral replay + mag3 (verbatim L6 GB-1) ----
    if "gb1" not in res["gates"]:
        dv3,mag3_=rung_edit_delta(3); dvm3,_=rung_edit_delta(-3)
        Mp3=onset_mean(injR,dv3); Mm3=onset_mean(injR,dvm3)
        A_on=(Mp3-Mm3)/2.0
        devA=abs(A_on-GB1_AON); devM=abs(mag3_-GB1_MAG3)
        gb1_ok=bool(devA<=TOL_REPLAY and devM<=TOL_MAG)
        Mcl=onset_mean(injR,torch.zeros(N_R,CERT_BLOCK,d))
        res["gates"]["gb1"]={"A_on":round(A_on,5),"banked_A":GB1_AON,"dev_A":round(devA,6),
            "mag3":round(mag3_,4),"banked_mag3":GB1_MAG3,"dev_mag":round(devM,5),
            "M_plus3":round(Mp3,5),"M_minus3":round(Mm3,5),
            "M_clean":round(Mcl,5),"banked_M_clean":GB2_MCLEAN,"pass":gb1_ok}
        if not gb1_ok and not SMOKE:
            flag("gb1","GB-1_rung_replay",res["gates"]["gb1"])
            res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-B: GB-1 rung replay failed")
        write_json(); logln(f"[GB-1] A_on={A_on:.5f} (banked {GB1_AON}) mag3={mag3_:.4f} Mclean={Mcl:.5f} -> {'PASS' if gb1_ok else 'FAIL(smoke)'}")
    gb1=res["gates"]["gb1"]; mag3=gb1["mag3"]; A_on=gb1["A_on"]

    # ---- shared null kernel (verbatim L6 onset_null; generator passed in) ----
    def onset_null(gen,mag,n,tag):
        vals=[]
        for it in range(n):
            r=torch.randn(d,generator=gen,device='cuda'); r=r/r.norm().clamp(min=1e-6)
            dp=(mag*r).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous(); dp=dp.clone(); dp[:, :IND_SEG, :]=0.0
            dm=(-mag*r).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous(); dm=dm.clone(); dm[:, :IND_SEG, :]=0.0
            vals.append(abs((onset_mean(injR,dp)-onset_mean(injR,dm))/2.0))
            logln(f"[{tag} null mag={mag:.2f} {it+1}/{n}] |A|={vals[-1]:.5f}")
        return vals

    # ---- M3 NULL-REPLAY GATE: reproduce L6's null95_20_mag3 (SEED_OQ4; discard mag6 stream) ----
    if "null95_replay" not in res["m3_replay"]:
        gpu_free_check("m3")
        gpQ=torch.Generator(device='cuda').manual_seed(SEED_OQ4)
        for _ in range(N_DISCARD):                    # the L6 mag6 stream consumed these 20 draws
            r=torch.randn(d,generator=gpQ,device='cuda')
        n_replay=N_NULL if SMOKE else 20
        nulls3_replay=onset_null(gpQ,mag3,n_replay,"M3-replay")
        null95_replay=pct95(nulls3_replay)
        dev=abs(round(null95_replay,5)-L6_NULL95_20_MAG3)
        m3_ok=bool(dev<=TOL_NULLREPLAY) if not SMOKE else True
        res["m3_replay"]={"null95_replay":round(null95_replay,5),"banked":L6_NULL95_20_MAG3,
            "dev":round(dev,7),"n":n_replay,"nulls":[round(x,5) for x in nulls3_replay],"pass":m3_ok}
        if not m3_ok: flag("m3","FB-C_null_replay_dev",res["m3_replay"])
        write_json(); logln(f"[M3] null95_replay={null95_replay:.5f} (banked {L6_NULL95_20_MAG3}) dev={dev:.7f} -> {'PASS' if m3_ok else 'FLAGGED'}")

    # ---- M4 FRESH RE-DRAW (the deliverable): SEED_N20, 20 fresh draws at mag3 ----
    if "null95_20_new" not in res["m4_fresh"]:
        gpu_free_check("m4")
        gpF=torch.Generator(device='cuda').manual_seed(SEED_N20)
        nulls_new=onset_null(gpF,mag3,N_NULL,"M4-fresh")
        null95_new=pct95(nulls_new)
        res["m4_fresh"]={"null95_20_new":round(null95_new,5),"n":N_NULL,"seed":SEED_N20,
            "nulls":[round(x,5) for x in nulls_new],
            "null_mean":round(sum(nulls_new)/len(nulls_new),5)}
        write_json(); logln(f"[M4] null95_20_new={null95_new:.5f} (n={N_NULL} seed={SEED_N20})")

    # ---- VERDICT (mechanical; pre-reg bands) ----
    null95_new=res["m4_fresh"]["null95_20_new"]
    R=abs(A_on)/null95_new if null95_new>0 else float('inf')
    band=("BEATS" if R>1.1 else ("KNIFE-EDGE" if R>=0.9 else "BELOW"))
    res["verdict"]={"A_on":A_on,"abs_A_on":round(abs(A_on),5),"null95_20_new":null95_new,
        "ratio_R":round(R,4),"band":band,
        "replaced_disclosure":{"L5_null95_N3":L5_NULL95_N3,"L6_rearm_null95_20":L6_NULL95_20_MAG3},
        "binding_rule":"verdicts untouched in every branch: the rung stays steering-unusable "
                       "(zero internal readouts cleared, sub-linear dose scaling); this run only "
                       "replaces the N=3 null disclosure.",
        "smoke":SMOKE}
    res["status"]="SMOKE-OK" if SMOKE else "COMPLETE"
    write_json()
    logln(f"[VERDICT] |A_on|={abs(A_on):.5f} vs null95_20_new={null95_new:.5f} -> R={R:.4f} -> {band}")
    injR.close()
    if not SMOKE:
        with open(os.path.join(DIR,"_l5n20.done"),"w") as f: f.write(f"{band} R={R:.4f}\n")
        logln("[done] _l5n20.done written LAST")
    logln(f"L5N20 END status={res['status']} elapsed={el()}s")
except Exception as e:
    res["status"]="ERROR"; res["error"]=traceback.format_exc(); write_json()
    logln("ERROR:\n"+traceback.format_exc()); raise
