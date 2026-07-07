# _l5.py -- L5 FINISH THE TWO BABEL REMAINDERS. PROPOSE-ONLY. GPT-2 124M.
# Pre-registration: FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md ::
#   "L5 -- FINISH THE TWO BABEL REMAINDERS ... ARM A TRANSPLANT-GAP ATTRIBUTION + ARM B
#    RUNG-STEERING-VIA-MATCHED-CHANNELS -- GAP-SCAN + PRE-REGISTRATION (2026-07-06)".
# Brief: L5_BRIEF_2026-07-06.md (Will 2026-07-06). ALL machinery byte-verbatim from _l4.py / _l3.py
#   (model loader / capture_h_all / proj_compl / wte_y4 / fkl / InjectHook additive residual at BUS[b] /
#   inject_kl_full / inject_kl_pidx / the T2 transplant metric / the rung edit_delta / wu_image) AND
#   from _l1.py (CH-INT logit-lens contrast + CH-FIELD content-field readouts). L5 changes ONLY *what*
#   is transplanted (Arm A payloads) and *what* is measured (Arm B behavioral onset + matched channels).
# Consumes FROZEN ENCODER_V1 (_l3_encoder.pt 6be189567c41e91d). No weights trained. decoder_v7 b1d2f464c00c3ef6.
import json, time, os, math, traceback, gc, subprocess, hashlib, ctypes
import torch, torch.nn as nn, torch.nn.functional as Fnn

t0=time.time()
DIR=r"C:\Shadow\Dissector\D0_PROGRAM\CONSTRUCTIVE"
SMOKE=os.environ.get("L5_SMOKE")=="1"
LOG=open(os.path.join(DIR,"_l5.log"),"a",encoding="utf-8")
def logln(s):
    s=str(s); LOG.write(f"[L5 {round(time.time()-t0,1):8.1f}s] "+s+"\n"); LOG.flush()
    try: print(s,flush=True)
    except Exception: pass
def el(): return round(time.time()-t0,1)
logln("="*100); logln(f"L5 START smoke={SMOKE} torch={torch.__version__}")
try:
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(),0x4000)
    logln("[ops] priority BelowNormal set")
except Exception as e: logln(f"[ops] priority set failed: {e}")
torch.set_num_threads(6)

# ---------------- locked constants (verbatim v7/l3/l4) ----------------
EPS_KL=0.1871; CERT_BLOCK=512; IND_SEG=64; MB=4; CAP_CHUNK=16
VOCAB_SANS_SPECIALS=50256; REGIMES=["prose","code","repetition"]
FRESH_LO,FRESH_HI=24576,32768; REP_SEED=3
N_HOLD=16; TOL_REPLAY=2e-3
DEC_V7_SHA="b1d2f464c00c3ef6"; ENC_SHA="6be189567c41e91d"
N_NULLDIR=1 if SMOKE else 3
K_EDIT=[3,-3] if SMOKE else [3,-3,6,-6]        # +/-3 verdict antisym; +/-6 dose (report-only)
L4_T2_SBAR=0.9467                                # L4 T2 gate anchor (byte-replay target)
SOFT_WALL_S=5*3600
FIELD_BOUNDS=[5,6,7,8]                           # CH-FIELD uses b5,b6 ; CH-INT uses b6,b7,b8
FIELD_NAMES={0:"naval/warship",5:"clause-final/physical-process"}

RESULT_JSON=os.path.join(DIR,"_l5_result_SMOKE.json" if SMOKE else "_l5_result.json")
BASES_PT=os.path.join(DIR,"_l5_bases_SMOKE.pt" if SMOKE else "_l5_bases.pt")
torch.manual_seed(1234)

PEN=("FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md :: 'L5 -- FINISH THE TWO BABEL REMAINDERS: ARM A "
     "TRANSPLANT-GAP ATTRIBUTION + ARM B RUNG-STEERING-VIA-MATCHED-CHANNELS -- GAP-SCAN + "
     "PRE-REGISTRATION (2026-07-06)'")
res={"experiment":"L5 finish the two Babel remainders: Arm A transplant gap attribution (3 nested "
     "payloads readable/certified-door/full-raw, gate payload-1==L4 T2 0.9467, matched-random nulls, "
     "captured-mass table); Arm B rung steering via matched channels (behavioral onset metric M_onset + "
     "CH-INT/CH-FIELD, positive-control gate, matched-random + magnitude-matched nulls). Consumes FROZEN "
     "ENCODER_V1. GPT-2 124M.","date":"2026-07-06","propose_only":True,"pre_registration":PEN,
     "locked":{"tol_replay":TOL_REPLAY,"n_nulldir":N_NULLDIR,"k_edit":K_EDIT,"l4_t2_sbar":L4_T2_SBAR,
        "armA_bands":"phi=(sbar2-sbar1)/(sbar3-sbar1): ATTRIBUTED phi>=0.75 / PARTIAL 0.25<phi<0.75 / "
                     "MISSING-MASS phi<=0.25 ; bet PARTIAL40/MISSING35/ATTRIBUTED25 ; gate sbar1==0.9467+-2e-3",
        "armB_bands":"positive-control GATE first; STEERS-BEHAVIORAL if behavioral_steers / CHANNEL-SPECIFIC "
                     "if int_or_field_clear only / CERTIFIED-READ-ONLY if inert all channels ; "
                     "bet STEERS40/CHANNEL25/READONLY35"},
     "config":{"n_hold":N_HOLD,"mb":MB,"cap_chunk":CAP_CHUNK,"cert_block":CERT_BLOCK,"ind_seg":IND_SEG,
        "precision":"fp32","tf32":"off","attn":"eager","seed":1234,"smoke":SMOKE},
     "gpu_free_checks":[],"instrument_discrepancy":[],"gates":{},
     "armA":{},"armB":{},"status":"INIT"}

def write_json():
    res["elapsed_s"]=el(); tmp=RESULT_JSON+".tmp"
    with open(tmp,"w",encoding="utf-8") as f: json.dump(res,f,indent=1,default=str)
    os.replace(tmp,RESULT_JSON)
BASES={}
def save_bases():
    tmp=BASES_PT+".tmp"; torch.save(BASES,tmp); os.replace(tmp,BASES_PT)

# ---------------- resume ----------------
if os.path.exists(RESULT_JSON):
    try:
        prev=json.load(open(RESULT_JSON,encoding="utf-8"))
        for k in ("armA","armB","gates","gpu_free_checks","instrument_discrepancy"):
            if prev.get(k): res[k]=prev[k]
        logln(f"*** RESUME *** armA={list(res['armA'].keys())} armB={list(res['armB'].keys())}")
    except Exception as e: logln(f"resume load fail {e}")
if os.path.exists(BASES_PT):
    try: BASES=torch.load(BASES_PT,map_location="cpu",weights_only=False)
    except Exception as e: logln(f"bases resume fail {e}"); BASES={}
write_json()

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

# ---------------- model (v7/l4 loader verbatim) ----------------
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

def load_wiki_text():
    from datasets import load_dataset
    ds=load_dataset("wikitext","wikitext-2-raw-v1",split="test")
    return "\n".join(t for t in ds["text"] if t and t.strip())
def load_code_text():
    from datasets import load_dataset
    ds=load_dataset("openai_humaneval")["test"]
    return "".join(ds[i]["prompt"]+ds[i]["canonical_solution"] for i in range(len(ds)))
def build_dind(n_blocks,block,seed):
    g=torch.Generator().manual_seed(seed)
    seg=torch.randint(0,VOCAB_SANS_SPECIALS,(n_blocks,IND_SEG),generator=g)
    return seg.repeat(1,block//IND_SEG)
def ids_window(all_ids,lo,hi,what):
    if len(all_ids)<hi: raise RuntimeError(f"{what}: {len(all_ids)}<{hi}")
    n=(hi-lo)//CERT_BLOCK; return torch.tensor(all_ids[lo:hi],dtype=torch.long).view(n,CERT_BLOCK)

# ---------------- KL kernel + inject (v7/l4 verbatim) ----------------
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

# capture selected boundary outputs UNDER an additive inject (MB-batched to match the metric shape)
def capture_under_delta(ids_cpu,injhook,delta_full_g,want_bounds):
    model=M["m"]; N=ids_cpu.shape[0]; d=M["d"]; buf={}
    def mk(key):
        def h(mod,inp,out): buf[key]=(out[0] if isinstance(out,tuple) else out).detach()
        return h
    hh=[]
    for b in want_bounds:
        blk=(M["blocks"][b-1] if b>=1 else M["drop"]); hh.append(blk.register_forward_hook(mk(b)))
    acc={b:[] for b in want_bounds}
    with torch.no_grad():
        for s0 in range(0,N,MB):
            s1=min(N,s0+MB)
            if injhook is not None:
                injhook.add=delta_full_g[s0:s1].to('cuda').float(); injhook.on=True
            _=model(ids_cpu[s0:s1].to('cuda'),use_cache=False)
            if injhook is not None: injhook.on=False; injhook.add=None
            for b in want_bounds: acc[b].append(buf[b].reshape(-1,d).cpu())
    for x in hh: x.remove()
    return {b:torch.cat(acc[b]) for b in want_bounds}

class LinearRung(nn.Module):
    def __init__(self,fin,d): super().__init__(); self.w=nn.Linear(fin,d)
    def forward(self,x): return self.w(x)

# ======================================================================================
# MAIN
# ======================================================================================
try:
    ensure_model()
    d=M["d"]; nL=M["nL"]; tok=M["tok"]; wte_g=M["wte"]; lnf_g=M["lnf"].to('cuda'); lnf_cpu=M["lnf"].cpu()

    # ---- GATE-0: hashes ----
    encsha=sha256(os.path.join(DIR,"_l3_encoder.pt"))
    d7sha=sha256(os.path.join(DIR,"decoder_v7_tensors.pt"))
    frecsha=sha256(os.path.join(DIR,"_v5_floors_recal.json"))
    lexsha=sha256(os.path.join(DIR,"LEXICON_V3.md"))
    wpsha=sha256(os.path.join(DIR,"WELLPOSEDNESS_TABLE_V1.json"))
    ossha=sha256(os.path.join(DIR,"OFFSPAN_TABLE_V1.json"))
    encjsha=sha256(os.path.join(DIR,"ENCODER_V1.json"))
    enc_ok=(encsha==ENC_SHA); d7_ok=(d7sha==DEC_V7_SHA)
    res["gates"]["hashes"]={"encoder_v1":encsha,"encoder_ok":bool(enc_ok),"encoder_json":encjsha,
        "decoder_v7":d7sha,"decoder_v7_ok":bool(d7_ok),"floors_recal":frecsha,"lexicon_v3":lexsha,
        "wellposedness":wpsha,"offspan":ossha}
    logln(f"[GATE-0] enc {encsha} ok={enc_ok} dec {d7sha} ok={d7_ok} wp {wpsha}")
    write_json()
    if (not enc_ok or not d7_ok) and not SMOKE:
        res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-A: encoder/decoder hash mismatch")

    # ---- load decoder_v7 objects (verbatim l3/l4) ----
    D7=torch.load(os.path.join(DIR,"decoder_v7_tensors.pt"),map_location="cpu",weights_only=False)
    C=D7["C"].float(); B2=D7["B2"].float(); Q35=D7["Q35"].float(); Qu=D7["Q_union"].float()
    Qa=D7["Q_attn"].float(); Qm=D7["Q_mlp"].float()
    mu=D7["mu"].float(); wteW=D7["wte_W"].float(); wtec=D7["wte_c"].float()
    read_W=D7["read_W"].float(); Vk=D7["m0_repera_Vk_recal"].float()
    # ---- FROZEN ENCODER_V1 cross-check == decoder_v7 reader bases to machine precision ----
    ENC=torch.load(os.path.join(DIR,"_l3_encoder.pt"),map_location="cpu",weights_only=False)
    xcheck={}
    for nm,a,b in [("C",ENC["C"],C),("B2",ENC["B2"],B2),("Q35",ENC["Q35"],Q35),("Q_union",ENC["Q_union"],Qu),
                   ("mu",ENC["mu"],mu),("read_W",ENC["read_W"],read_W)]:
        xcheck[nm]=float((a.float()-b.float()).abs().max())
    enc_matches=all(v<=1e-6 for v in xcheck.values())
    readW_pinv=ENC["read_W_pinv"].float()   # [13,385,19] frozen right-inverse
    res["gates"]["encoder_is_decoder_inverse"]={"max_abs_diff":xcheck,"pass":bool(enc_matches)}
    logln(f"[GATE-0b] ENCODER_V1==decoder_v7 reader: {xcheck} -> {enc_matches}")
    if not enc_matches and not SMOKE:
        res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-A: encoder not decoder inverse")
    C_g=C.to('cuda'); B2_g=B2.to('cuda'); Q35_g=Q35.to('cuda'); span5=torch.cat([B2_g,Q35_g],1)
    Qu_g=Qu.to('cuda'); Vk_g=Vk.to('cuda'); mu_g={b:mu[b].to('cuda') for b in range(nL+1)}
    wteW_g=wteW.to('cuda'); wtec_g=wtec.to('cuda')
    read_W_g={b:read_W[b].to('cuda') for b in range(read_W.shape[0])}
    readW_pinv_g={b:readW_pinv[b].to('cuda') for b in range(readW_pinv.shape[0])}
    def load_rung(sd_key,scm_key,scs_key):
        r=LinearRung(1537,d).to('cuda').eval()
        r.load_state_dict({k:v.to('cuda').float() for k,v in D7[sd_key].items()})
        return r, D7[scm_key].to('cuda').float(), D7[scs_key].to('cuda').float()
    RUNG={}
    RUNG[("repetition",6)]=load_rung("onset_b6_state_dict","onset_b6_scaler_mean","onset_b6_scaler_std")
    frec=json.load(open(os.path.join(DIR,"_v5_floors_recal.json"),encoding="utf-8"))
    RECAL_OK=(not frec.get("quarantined")) and frec.get("sg_early_ok") and frec.get("repl_all")
    logln(f"[objects] loaded. RECAL_OK={RECAL_OK}")

    def proj_compl(x): return x-(x@span5)@span5.t()
    def wte_y4(ids_flat_g,b):
        Ecur=wte_g[ids_flat_g]; yhat=Ecur@wteW_g[b].t()+wtec_g[b]
        y2=yhat-(yhat@B2_g)@B2_g.t(); return y2-(y2@Q35_g)@Q35_g.t()
    def wu_image(v_g):
        col=wte_g@(v_g*lnf_g); return torch.topk(col,40).indices, torch.topk(-col,40).indices

    # regime holdout streams (verbatim)
    def build_regime_hold(regime):
        if regime=="prose":
            WIKI=tok(load_wiki_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
            return ids_window(WIKI,FRESH_LO,FRESH_LO+N_HOLD*CERT_BLOCK,"wiki hold")
        if regime=="code":
            CIDS=tok(load_code_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
            return ids_window(CIDS,FRESH_LO,FRESH_LO+N_HOLD*CERT_BLOCK,"code hold")
        if regime=="repetition":
            return build_dind(N_HOLD,CERT_BLOCK,REP_SEED)
        raise RuntimeError(regime)
    CAP={}; IDS={}; YCL={}
    def get_regime(regime):
        if regime not in CAP:
            ids=build_regime_hold(regime); IDS[regime]=ids
            CAP[regime]=capture_h_all(ids,f"reg-{regime}",extra_wm0=(regime=="repetition"))
            YCL[regime]=clean_logits(ids)
        return IDS[regime],CAP[regime],YCL[regime]
    def rep_feats(ids,cap):
        x2=cap[2].to('cuda')-mu_g[2]; ecur=wte_g[ids.reshape(-1).to('cuda')]; s=cap['wm0'].to('cuda')@Vk_g
        return x2,ecur,s

    # ================= GATE-0 identity-inject exact-zero per regime =================
    if not res["gates"].get("identity_inject"):
        id_regs=(["prose"] if SMOKE else REGIMES); id_sane=True; id_detail={}
        for regime in id_regs:
            ids,cap,Ycl=get_regime(regime)
            inj=InjectHook(M["blocks"][5])
            idkl,iddl=inject_kl_full(ids,inj,torch.zeros(ids.shape[0],CERT_BLOCK,d),Ycl,want_dl=True); inj.close()
            ok=bool(idkl<=1e-9 and iddl<=1e-4); id_sane=id_sane and ok
            id_detail[regime]={"kl":idkl,"dlogit":round(iddl,7),"pass":ok}
            logln(f"[GATE-0 identity {regime}] kl={idkl} dlogit={iddl} -> {ok}")
        res["gates"]["identity_inject"]={"detail":id_detail,"pass":bool(id_sane)}; write_json()
        if not id_sane and not SMOKE:
            res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-A: identity-inject not exact-zero")

    # =========================================================================================
    # ARM A -- TRANSPLANT GAP ATTRIBUTION (prose b6, 16 pairs, 3 nested payloads + matched-random null)
    # =========================================================================================
    if not res["armA"].get("done"):
        gpu_free_check("armA")
        b=6; regime="prose"
        ids,cap,Ycl=get_regime(regime); N=ids.shape[0]
        Xc=cap[b].to('cuda')-mu_g[b]; ids_flat_g=ids.reshape(-1).to('cuda')
        b2P=(Xc@B2_g)@B2_g.t(); q35P=(Xc@Q35_g)@Q35_g.t(); y4=wte_y4(ids_flat_g,b)
        # proper ORTHONORMAL projectors (Q_union only near-orthonormal; raw attn/mlp door bases reach the
        # dark complement). onb() = QR orthonormalization of a basis's column space.
        def onb(Mx): q,_=torch.linalg.qr(Mx); return q
        Uqu=onb(Qu_g)                                                   # ON basis of col(Q_union)
        Uraw=onb(torch.cat([Qa.to('cuda'),Qm.to('cuda')],1))           # ON basis of raw attn+mlp door bases
        # payload reconstructions (residual-space add-ons); recon in ABSOLUTE state
        recon1=(mu_g[b]+b2P+q35P+y4)                                    # readable gloss (L4 T2 payload)
        # certified door-summary read (rank<=19 through read_W[b] summarizer), orthogonal to span5
        c_door=Xc@Qu_g                                                  # [ntok,385] door coords
        g19=c_door@read_W_g[b].t()                                      # [ntok,19] certified summary read
        c_hat=g19@readW_pinv_g[b].t()                                   # [ntok,385]
        door19=c_hat@Qu_g.t()                                           # [ntok,768]
        door19_perp=proj_compl(door19)
        recon2=recon1+door19_perp                                       # readable + certified door read (VERDICT)
        qu_perp=proj_compl((Xc@Uqu)@Uqu.t())                           # full Q_union ON-proj beyond span5
        recon2b=recon1+qu_perp                                          # readable + full summarized door subspace
        raw_perp=proj_compl((Xc@Uraw)@Uraw.t())                        # raw attn/mlp door subspace beyond span5
        recon2c=recon1+raw_perp                                         # readable + raw (un-summarized) door subspace
        recon3=(mu_g[b]+Xc)                                             # full raw state (ceiling)
        # captured-mass table (share of mean ||Xc||^2) with PROPER projectors
        tot_m=float((Xc*Xc).sum(1).mean())
        read_m=float(((b2P+q35P)*(b2P+q35P)).sum(1).mean())
        door_inc_m=float((door19_perp*door19_perp).sum(1).mean())
        qu_inc_m=float((qu_perp*qu_perp).sum(1).mean())
        raw_inc_m=float((raw_perp*raw_perp).sum(1).mean())
        dark_m=float((proj_compl(Xc)*proj_compl(Xc)).sum(1).mean())     # mass orthogonal to span5
        res["armA"]["captured_mass"]={"total":round(tot_m,3),"readable_span5":round(read_m,3),
            "dark_orthogonal_span5":round(dark_m,3),"certified_door_summary_increment":round(door_inc_m,3),
            "qunion_onproj_increment":round(qu_inc_m,3),"raw_door_increment":round(raw_inc_m,3),
            "readable_frac":round(read_m/tot_m,4),"cert_door_inc_frac":round(door_inc_m/tot_m,4),
            "qunion_inc_frac":round(qu_inc_m/tot_m,4),"raw_door_inc_frac":round(raw_inc_m/tot_m,4),
            "dark_frac":round(dark_m/tot_m,4)}
        logln(f"[armA mass] read={read_m/tot_m:.3f} certdoor_inc={door_inc_m/tot_m:.4f} "
              f"qunion_inc={qu_inc_m/tot_m:.4f} rawdoor_inc={raw_inc_m/tot_m:.4f} dark={dark_m/tot_m:.3f}")
        recons={"p1_readable":recon1,"p2_certdoor":recon2,"p2b_qunion":recon2b,"p2c_rawdoor":recon2c,"p3_fullraw":recon3}
        pairs=([(0,1),(2,3)] if SMOKE else [(i,(i+1)%N) for i in range(N)])
        inj=InjectHook(M["blocks"][b-1])
        gp=torch.Generator(device='cuda').manual_seed(20260706)
        def klrow(pt,pp):
            logpt=Fnn.log_softmax(pt,-1); p=logpt.exp(); logpp=Fnn.log_softmax(pp,-1)
            return (p*(logpt-logpp)).sum(-1)
        for pname,recon_flat in recons.items():
            if pname in res["armA"].get("payloads",{}): continue
            recon=recon_flat.reshape(N,CERT_BLOCK,d)
            per_pair=[]
            for (ai,bi) in pairs:
                dstate=(recon[ai]-recon[bi])
                deltaB=torch.zeros(N,CERT_BLOCK,d,device='cuda'); deltaB[bi]=dstate
                with torch.no_grad():
                    lgA=M["m"](ids[ai:ai+1].to('cuda'),use_cache=False).logits[0].float()
                    lgB=M["m"](ids[bi:bi+1].to('cuda'),use_cache=False).logits[0].float()
                    inj.add=deltaB[bi:bi+1]; inj.on=True
                    lgInj=M["m"](ids[bi:bi+1].to('cuda'),use_cache=False).logits[0].float(); inj.on=False; inj.add=None
                klBA=klrow(lgB,lgA).clamp(min=1e-9); klInjA=klrow(lgInj,lgA)
                s=((klBA-klInjA)/klBA); s_mean=float(s.mean()); residKL=float(klInjA.mean())
                # matched-random null: random dir in the payload's reachable subspace at matched per-position norm
                snull=[]
                for _ in range(N_NULLDIR):
                    r=torch.randn(CERT_BLOCK,d,generator=gp,device='cuda')
                    if pname=="p1_readable": r=(r@span5)@span5.t()          # span5 (L4 T2 null, verbatim)
                    # p2/p2b/p3 reachable subspace is full-rank R^768 -> random full-space dir
                    nrm=r.norm(dim=1,keepdim=True).clamp(min=1e-9)
                    r=r/nrm*dstate.norm(dim=1,keepdim=True)
                    dn=torch.zeros(N,CERT_BLOCK,d,device='cuda'); dn[bi]=r
                    with torch.no_grad():
                        inj.add=dn[bi:bi+1]; inj.on=True
                        lgNn=M["m"](ids[bi:bi+1].to('cuda'),use_cache=False).logits[0].float(); inj.on=False; inj.add=None
                    snull.append(float(((klBA-klrow(lgNn,lgA))/klBA).mean()))
                per_pair.append({"A":ai,"B":bi,"s":round(s_mean,4),"s_null":round(sum(snull)/len(snull),4),
                                 "residKL":round(residKL,5)})
            import statistics as st
            sbar=sum(p["s"] for p in per_pair)/len(per_pair)
            sbar_null=sum(p["s_null"] for p in per_pair)/len(per_pair)
            residKL=sum(p["residKL"] for p in per_pair)/len(per_pair)
            se=(st.pstdev([p["s"] for p in per_pair])/math.sqrt(len(per_pair))) if len(per_pair)>1 else 0.0
            res["armA"].setdefault("payloads",{})[pname]={"sbar":round(sbar,4),"sbar_null":round(sbar_null,4),
                "se":round(se,4),"residKL":round(residKL,5),"n_pairs":len(pairs),"per_pair":per_pair}
            write_json(); logln(f"[armA {pname}] sbar={sbar:.4f} null={sbar_null:.4f} residKL={residKL:.5f}")
        inj.close()
        # verdict
        P=res["armA"]["payloads"]
        sbar1=P["p1_readable"]["sbar"]; sbar2=P["p2_certdoor"]["sbar"]; sbar3=P["p3_fullraw"]["sbar"]
        gate_dev=abs(sbar1-L4_T2_SBAR); gate_ok=bool(gate_dev<=TOL_REPLAY)
        if not gate_ok:
            res["instrument_discrepancy"].append({"stage":"armA","name":"payload1_replay",
                "why":f"sbar1={sbar1} L4={L4_T2_SBAR} dev={gate_dev}"})
        denom=(sbar3-sbar1)
        phi=((sbar2-sbar1)/denom) if abs(denom)>1e-6 else None
        if phi is None: verdict="DEGENERATE"
        elif phi>=0.75: verdict="ATTRIBUTED"
        elif phi<=0.25: verdict="MISSING-MASS"
        else: verdict="PARTIAL"
        res["armA"]["verdict"]={"sbar1":sbar1,"sbar2":sbar2,"sbar2b_qunion":P["p2b_qunion"]["sbar"],
            "sbar2c_rawdoor":P["p2c_rawdoor"]["sbar"],"sbar3":sbar3,
            "phi":(round(phi,4) if phi is not None else None),"H_L5_A":verdict,
            "gate_payload1_dev":round(gate_dev,5),"gate_ok":gate_ok,
            "residKL_p2_vs_floor":{"residKL_p2":P["p2_certdoor"]["residKL"],"recal_floor":EPS_KL,
                                    "within_floor":bool(P["p2_certdoor"]["residKL"]<=EPS_KL)},
            "bet":"PARTIAL40/MISSING35/ATTRIBUTED25","bet_favorite_hit":bool(verdict=="PARTIAL")}
        res["armA"]["done"]=True; write_json()
        logln(f"[armA VERDICT] phi={phi} sbar1={sbar1} sbar2={sbar2} sbar3={sbar3} gate_ok={gate_ok} -> {verdict}")
        del Xc,b2P,q35P,y4,recon1,recon2,recon2b,recon3,door19,door19_perp; free()

    # =========================================================================================
    # ARM B -- RUNG STEERING VIA MATCHED CHANNELS (behavioral onset + CH-INT/CH-FIELD; positive control)
    # =========================================================================================
    if not res["armB"].get("done"):
        gpu_free_check("armB")
        bb=6; rg="repetition"
        ids,cap,Ycl=get_regime(rg); N=ids.shape[0]
        # onset metric: mean over positions [IND_SEG, CERT_BLOCK-1) of P(model predicts correct repeat token)
        def onset_perpos(injhook,delta_full_g):
            # returns [N, CERT_BLOCK-1-IND_SEG] repeat-token probs (positions IND_SEG..CERT_BLOCK-2)
            model=M["m"]; out=[]
            with torch.no_grad():
                for s0 in range(0,N,MB):
                    s1=min(N,s0+MB)
                    if injhook is not None: injhook.add=delta_full_g[s0:s1].to('cuda').float(); injhook.on=True
                    lg=model(ids[s0:s1].to('cuda'),use_cache=False).logits.float()
                    if injhook is not None: injhook.on=False; injhook.add=None
                    lp=Fnn.log_softmax(lg,-1)
                    tgt=ids[s0:s1,1:].to('cuda')                                  # next tokens [b,511]
                    sl=lp[:,IND_SEG:CERT_BLOCK-1,:].gather(-1,tgt[:,IND_SEG:CERT_BLOCK-1].unsqueeze(-1)).squeeze(-1).exp()
                    out.append(sl.cpu()); del lg,lp
            return torch.cat(out)                                                 # [N, 447]
        def onset_mean(injhook,delta_full_g): return float(onset_perpos(injhook,delta_full_g).mean())

        inj=InjectHook(M["blocks"][bb-1])   # BUS[6] = block 5 output
        # ----- rung edit_delta (byte-verbatim L4 T3 rung path) -----
        x2,ecur,s=rep_feats(ids,cap); feats=torch.cat([x2,ecur,s],1)
        rung,scm,scs=RUNG[(rg,bb)]
        with torch.no_grad(): oh_real=proj_compl(rung((feats-scm)/scs))
        sig_s=float(s.std())
        def rung_edit_delta(k):
            s2=s+k*sig_s; feats2=torch.cat([x2,ecur,s2],1)
            with torch.no_grad(): ohp=proj_compl(rung((feats2-scm)/scs))
            dv=(ohp-oh_real).reshape(N,CERT_BLOCK,d).contiguous(); dv=dv.clone(); dv[:, :IND_SEG, :]=0.0
            mag=float(dv[:, IND_SEG:, :].reshape(-1,d).norm(dim=1).mean())
            return dv,mag
        # rung readout column (L4 T3 verbatim): mean onset-b6 output direction
        rung_img_dir=oh_real.mean(0); rung_img_dir=rung_img_dir/rung_img_dir.norm().clamp(min=1e-6)
        top,bot=wu_image(rung_img_dir); Wtop=wte_g[top]; Wbot=wte_g[bot]

        # ----- clean onset baseline + per-position (for positive control axis) -----
        if "onset_clean" not in res["armB"]:
            pp_clean=onset_perpos(None,None)                                      # [N,447]
            res["armB"]["onset_clean"]=round(float(pp_clean.mean()),5); write_json()
            BASES["armB_onset_clean_perpos"]=pp_clean
            logln(f"[armB] onset clean M_onset={res['armB']['onset_clean']}")
        else:
            pp_clean=BASES.get("armB_onset_clean_perpos")
            if pp_clean is None: pp_clean=onset_perpos(None,None)
        M_clean=res["armB"]["onset_clean"]

        # ----- POSITIVE CONTROL: empirical onset direction v_onset (pre->post via high/low repeat-prob).
        # GATE at the NATURAL data-scale onset displacement (guaranteed behaviorally meaningful -> proves the
        # M_onset pipeline registers a BUS[6]-injected onset change). ALSO report a rung-magnitude-matched
        # (mag3) control so rung-vs-control is a fair same-magnitude comparison. -----
        if "positive_control" not in res["armB"]:
            posrange=torch.arange(IND_SEG,CERT_BLOCK-1)
            Xc6=(cap[bb].to('cuda')-mu_g[bb]).reshape(N,CERT_BLOCK,d)[:,posrange,:].reshape(-1,d)  # [N*447,d]
            probs=pp_clean.reshape(-1).to('cuda')                                  # [N*447], aligned to Xc6
            k_sel=max(1,int(0.25*probs.numel()))
            hi=torch.topk(probs,k_sel).indices; lo=torch.topk(-probs,k_sel).indices
            v_raw=(Xc6[hi].mean(0)-Xc6[lo].mean(0)); nat_mag=float(v_raw.norm())    # natural onset shift scale
            v_onset=v_raw/v_raw.norm().clamp(min=1e-6)
            _,mag3=rung_edit_delta(3)                                              # rung native magnitude
            def onset_dir_delta(sign,mag):
                dv=(sign*mag*v_onset).view(1,1,d).expand(N,CERT_BLOCK,d).contiguous()
                dv=dv.clone(); dv[:, :IND_SEG, :]=0.0; return dv
            def run_ctrl(mag,seed):
                Mp=onset_mean(inj,onset_dir_delta(+1.0,mag)); Mm=onset_mean(inj,onset_dir_delta(-1.0,mag))
                A=(Mp-Mm)/2.0
                gpc=torch.Generator(device='cuda').manual_seed(seed); nl=[]
                for _ in range(N_NULLDIR):
                    r=torch.randn(d,generator=gpc,device='cuda'); r=r/r.norm().clamp(min=1e-6)
                    dp=(mag*r).view(1,1,d).expand(N,CERT_BLOCK,d).contiguous(); dp=dp.clone(); dp[:, :IND_SEG, :]=0.0
                    dm=(-mag*r).view(1,1,d).expand(N,CERT_BLOCK,d).contiguous(); dm=dm.clone(); dm[:, :IND_SEG, :]=0.0
                    nl.append(abs((onset_mean(inj,dp)-onset_mean(inj,dm))/2.0))
                n95=pct95(nl)
                ok=bool(abs(A)>n95 and (Mp-M_clean)*(M_clean-Mm)>0 and abs(A)>1e-4)
                return {"M_plus":round(Mp,5),"M_minus":round(Mm,5),"A":round(A,5),"null95":round(n95,5),
                        "mag":round(mag,4),"pass":ok}
            validity=run_ctrl(nat_mag,20260706)                                    # GATE (data-scale)
            matched=run_ctrl(mag3,20260706+1)                                      # fair same-mag-as-rung
            ctrl_pass=bool(validity["pass"])
            res["armB"]["positive_control"]={"M_clean":M_clean,"nat_mag":round(nat_mag,4),
                "validity_natural_mag":validity,"matched_rung_mag":matched,"GATE_PASS":ctrl_pass}
            write_json(); logln(f"[armB pos-control] validity(mag={nat_mag:.2f}) A={validity['A']} pass={validity['pass']} "
                                f"| matched(mag={mag3:.2f}) A={matched['A']} pass={matched['pass']} -> GATE={ctrl_pass}")

        # ----- BEHAVIORAL: rung edit onset ladder + matched-random / magnitude-matched nulls -----
        if "behavioral" not in res["armB"]:
            Mk={}
            for k in K_EDIT:
                dv,mag=rung_edit_delta(k); Mk[k]={"M":round(onset_mean(inj,dv),5),"mag":round(mag,4)}
                logln(f"[armB behavioral k={k}] M_onset={Mk[k]['M']} mag={Mk[k]['mag']}")
            A_on=(Mk[3]["M"]-Mk[-3]["M"])/2.0
            A_on6=((Mk[6]["M"]-Mk[-6]["M"])/2.0) if (6 in Mk and -6 in Mk) else None
            # SE over blocks at +/-3 (per-block onset mean)
            dvp,_=rung_edit_delta(3); dvm,_=rung_edit_delta(-3)
            pp_p=onset_perpos(inj,dvp).mean(1); pp_m=onset_perpos(inj,dvm).mean(1)          # [N] per-block
            a_block=((pp_p-pp_m)/2.0); se_on=float(a_block.std(unbiased=True)/math.sqrt(N))
            # matched-random-edit null on M_onset (random unit residual matched to rung mag3)
            _,mag3=rung_edit_delta(3)
            gpn=torch.Generator(device='cuda').manual_seed(20260706+7)
            onset_nulls=[]
            for _ in range(N_NULLDIR):
                r=torch.randn(d,generator=gpn,device='cuda'); r=r/r.norm().clamp(min=1e-6)
                dp=(mag3*r).view(1,1,d).expand(N,CERT_BLOCK,d).contiguous(); dp=dp.clone(); dp[:, :IND_SEG, :]=0.0
                dm=(-mag3*r).view(1,1,d).expand(N,CERT_BLOCK,d).contiguous(); dm=dm.clone(); dm[:, :IND_SEG, :]=0.0
                onset_nulls.append(abs((onset_mean(inj,dp)-onset_mean(inj,dm))/2.0))
            null95_on=pct95(onset_nulls); mag_matched_null=sum(onset_nulls)/len(onset_nulls)
            sign_repro=bool(A_on6 is None or (A_on*A_on6>0))
            behavioral_steers=bool(abs(A_on)>null95_on and abs(A_on)>=2*se_on and sign_repro)
            # token image at structured sign (which repeat/vocab tokens rise) -- demo
            k_show=3 if A_on>=0 else -3
            dvs,_=rung_edit_delta(k_show)
            with torch.no_grad():
                model=M["m"]; mlt=torch.zeros(wte_g.shape[0],device='cuda'); mc=0
                for s0 in range(0,N,MB):
                    s1=min(N,s0+MB); inj.add=dvs[s0:s1]; inj.on=True
                    lg=model(ids[s0:s1].to('cuda'),use_cache=False).logits.float(); inj.on=False; inj.add=None
                    base=Ycl[s0//MB].float()
                    dd=(lg[:,IND_SEG:CERT_BLOCK,:]-base[:,IND_SEG:CERT_BLOCK,:]); mlt+=dd.reshape(-1,dd.shape[-1]).sum(0)
                    mc+=dd.shape[0]*dd.shape[1]; del lg
                mlt=mlt/max(1,mc)
            risers=[tok.decode([int(i)]) for i in torch.topk(mlt,8).indices.tolist()]
            fallers=[tok.decode([int(i)]) for i in torch.topk(-mlt,8).indices.tolist()]
            res["armB"]["behavioral"]={"M_clean":M_clean,"ladder":{str(k):Mk[k]["M"] for k in Mk},
                "A_on":round(A_on,5),"A_on6":(round(A_on6,5) if A_on6 is not None else None),
                "se_on":round(se_on,5),"null95":round(null95_on,5),"mag_matched_null":round(mag_matched_null,5),
                "sign_reproducible":sign_repro,"beats_null":bool(abs(A_on)>null95_on),
                "beats_2se":bool(abs(A_on)>=2*se_on),"behavioral_steers":behavioral_steers,
                "edit_sign_shown":k_show,"tokens_risen":risers,"tokens_fell":fallers}
            write_json(); logln(f"[armB behavioral] A_on={A_on:.5f} null95={null95_on:.5f} 2se={2*se_on:.5f} "
                                f"signrepro={sign_repro} -> STEERS={behavioral_steers} risen={risers[:5]}")

        # ----- CH-INT + CH-FIELD (L1 verbatim readouts, under the additive rung actuator; CPU contraction
        # exactly as _l1.py: capm/cap0 are CPU, class + content bases pulled to CPU) -----
        if "matched_channels" not in res["armB"]:
            int_blocks=[x for x in (bb,bb+1,bb+2) if x<=nL-1]                      # boundaries 6,7,8
            want=sorted(set([bb-1]+int_blocks))                                    # 5,6,7,8
            pos=torch.arange(IND_SEG,CERT_BLOCK)                                    # rung metered positions
            v_c=rung_img_dir.cpu(); B2_c=B2; lnf_c=lnf_cpu                          # CPU bases (B2 is cpu)
            Wtop_c=Wtop.cpu(); Wbot_c=Wbot.cpu()
            cap0=capture_under_delta(ids,None,torch.zeros(N,CERT_BLOCK,d),want)     # clean captures (invariant)
            def caps_for(k):
                dv,_=rung_edit_delta(k); return capture_under_delta(ids,inj,dv,want)
            def _sl(cx,cy,kb): return (cx[kb]-cy[kb]).reshape(N,CERT_BLOCK,d)[:,pos,:].reshape(-1,d)
            def readouts_from(cP,cM,Wt,Wb,vv):
                ints={}
                for kb in int_blocks:
                    dk=((_sl(cP,cap0,kb)-_sl(cM,cap0,kb))/2.0)                      # antisym state delta (CPU)
                    dkl=dk*lnf_c
                    ct=(dkl@Wt.t()).mean(-1)-(dkl@Wb.t()).mean(-1)
                    ints[kb+1]={"C":float(ct.mean()),"SE":float(ct.std(unbiased=True)/math.sqrt(ct.numel()))}
                dcP=(_sl(cP,cap0,bb)-_sl(cP,cap0,bb-1)); dcP=dcP-(dcP@vv)[:,None]*vv[None,:]; Dp=(dcP@B2_c).mean(0)
                dcM=(_sl(cM,cap0,bb)-_sl(cM,cap0,bb-1)); dcM=dcM-(dcM@vv)[:,None]*vv[None,:]; Dm=(dcM@B2_c).mean(0)
                cos=float((Dp@Dm)/max(1e-12,float(Dp.norm())*float(Dm.norm()))); Dmag=float((Dp-Dm).norm()/2.0)
                return ints,{"cos":cos,"Dmag":Dmag}
            i1,f1=readouts_from(caps_for(3),caps_for(-3),Wtop_c,Wbot_c,v_c)
            i2,f2=(readouts_from(caps_for(6),caps_for(-6),Wtop_c,Wbot_c,v_c) if (6 in K_EDIT and -6 in K_EDIT) else (None,None))
            # matched-random-edit nulls for CH-INT and CH-FIELD (random dir, matched mag; own class/dir per draw)
            _,mag3=rung_edit_delta(3)
            gpi=torch.Generator(device='cuda').manual_seed(20260706+13)
            null_int=[]; null_D=[]
            for _ in range(N_NULLDIR):
                r=torch.randn(d,generator=gpi,device='cuda'); r=r/r.norm().clamp(min=1e-6)
                colr=wte_g@(r*lnf_g); topr=torch.topk(colr,40).indices; botr=torch.topk(-colr,40).indices
                Wtr=wte_g[topr].cpu(); Wbr=wte_g[botr].cpu(); rc=r.cpu()
                def capr(sign):
                    dv=(sign*mag3*r).view(1,1,d).expand(N,CERT_BLOCK,d).contiguous(); dv=dv.clone(); dv[:, :IND_SEG, :]=0.0
                    return capture_under_delta(ids,inj,dv,want)
                cP=capr(1.0); cM=capr(-1.0)
                mx=0.0
                for kb in int_blocks:
                    dk=((_sl(cP,cap0,kb)-_sl(cM,cap0,kb))/2.0)*lnf_c
                    ct=(dk@Wtr.t()).mean(-1)-(dk@Wbr.t()).mean(-1); mx=max(mx,abs(float(ct.mean())))
                null_int.append(mx)
                dcP=(_sl(cP,cap0,bb)-_sl(cP,cap0,bb-1)); dcP=dcP-(dcP@rc)[:,None]*rc[None,:]; Dp=(dcP@B2_c).mean(0)
                dcM=(_sl(cM,cap0,bb)-_sl(cM,cap0,bb-1)); dcM=dcM-(dcM@rc)[:,None]*rc[None,:]; Dm=(dcM@B2_c).mean(0)
                null_D.append(float((Dp-Dm).norm()/2.0))
            null95I=pct95(null_int); null95D=pct95(null_D)
            kstar=max(i1,key=lambda kk:abs(i1[kk]["C"])); mxi1=abs(i1[kstar]["C"])
            i1k=i1[kstar]; i2k=(i2[kstar] if i2 else None)
            int_clear=bool(mxi1>null95I and abs(i1k["C"])>=2*i1k["SE"])
            int_stable=bool(int_clear and i2k is not None and (i1k["C"]*i2k["C"]>0) and abs(i2k["C"])>=2*i2k["SE"])
            # FB-E: CH-FIELD is structurally ~0 for the rung (output proj_compl -> orthogonal to B2, and b5 is
            # upstream of the BUS[6] inject); guard the clear test against noise below an absolute content-field
            # floor so a ~0 field cannot spuriously "clear" and drive a false CHANNEL-SPECIFIC verdict.
            FIELD_ABS_FLOOR=1e-3
            field_degenerate=bool(f1["Dmag"]<FIELD_ABS_FLOOR)
            field_clear=bool((not field_degenerate) and f1["cos"]<=-0.5 and f1["Dmag"]>null95D)
            field_stable=bool(field_clear and f2 is not None and f2["cos"]<=-0.5)
            res["armB"]["matched_channels"]={
                "CH_INT":{"int1":{str(k):{"C":round(v_["C"],5),"SE":round(v_["SE"],5)} for k,v_ in i1.items()},
                          "int2":({str(k):{"C":round(v_["C"],5),"SE":round(v_["SE"],5)} for k,v_ in i2.items()} if i2 else None),
                          "kstar":int(kstar),"maxint1":round(mxi1,5),"null95":round(null95I,5),
                          "int_clear":int_clear,"int_stable":int_stable},
                "CH_FIELD":{"cos1":round(f1["cos"],4),"Dmag1":round(f1["Dmag"],6),
                            "cos2":(round(f2["cos"],4) if f2 else None),"Dmag2":(round(f2["Dmag"],6) if f2 else None),
                            "null95_D":round(null95D,6),"field_degenerate":field_degenerate,
                            "field_clear":field_clear,"field_stable":field_stable,
                            "note":"rung output proj_compl -> orthogonal to B2 & b5 upstream of BUS[6] inject -> "
                                   "content-field structurally ~0 (Dmag<1e-3 => UNMEASURABLE, not a silent pass)"}}
            write_json(); logln(f"[armB channels] INT clear={int_clear} kstar={kstar} maxC={mxi1:.5f} null95I={null95I:.5f} "
                                f"| FIELD clear={field_clear} cos={f1['cos']:.3f} Dmag={f1['Dmag']:.5f}")
        inj.close()

        # ----- Arm B verdict -----
        pc=res["armB"]["positive_control"]["GATE_PASS"]
        beh=res["armB"]["behavioral"]["behavioral_steers"]
        intc=res["armB"]["matched_channels"]["CH_INT"]["int_clear"]
        fldc=res["armB"]["matched_channels"]["CH_FIELD"]["field_clear"]
        if not pc:
            verdict="NO-VERDICT-PIPELINE-BROKEN"
        elif beh:
            verdict="STEERS-BEHAVIORAL"
        elif intc or fldc:
            verdict="CHANNEL-SPECIFIC"
        else:
            verdict="CERTIFIED-READ-ONLY"
        res["armB"]["verdict"]={"positive_control_pass":pc,"behavioral_steers":beh,"int_clear":intc,
            "field_clear":fldc,"H_L5_B":verdict,"bet":"STEERS40/CHANNEL25/READONLY35",
            "bet_favorite_hit":bool(verdict=="STEERS-BEHAVIORAL")}
        res["armB"]["done"]=True; write_json()
        logln(f"[armB VERDICT] pc={pc} beh={beh} int={intc} field={fldc} -> {verdict}")

    # ================= STATUS =================
    if SMOKE:
        okA=bool(res["armA"].get("done")); okB=bool(res["armB"].get("done"))
        res["status"]="SMOKE-"+("OK" if (okA and okB) else "FAIL")
    else:
        done=(res["armA"].get("done") and res["armB"].get("done"))
        res["status"]=("COMPLETE" if (done and not res["instrument_discrepancy"]) else
                       ("COMPLETE-WITH-DISCREPANCY" if done else "PARTIAL"))
    BASES["armA"]=res["armA"].get("verdict"); BASES["armB"]=res["armB"].get("verdict")
    save_bases(); write_json()
    if M["m"] is not None: del M["m"]; M["m"]=None; free()
except Exception as e:
    res["fatal_error"]={"error":str(e),"trace":traceback.format_exc()}
    logln(f"FATAL {e}\n{traceback.format_exc()}"); res.setdefault("status","FATAL")
write_json()
logln(f"L5 END status={res.get('status')} elapsed={el()}s armA={res['armA'].get('verdict',{}).get('H_L5_A')} "
      f"armB={res['armB'].get('verdict',{}).get('H_L5_B')}")
open(os.path.join(DIR,"_l5_smoke_gpu.done" if SMOKE else "_l5_gpu.done"),"w").write(str(res.get("status","?"))+"\n")
logln("*** L5_"+("SMOKE_" if SMOKE else "")+"DONE ***"); LOG.flush(); LOG.close(); print("done")
