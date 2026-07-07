# _l4.py -- L4 THE SPEAK TEST (Babel Stage 4, the crown). PROPOSE-ONLY. GPT-2 124M.
# Pre-registration: FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md ::
#   "L4 -- THE SPEAK TEST (BABEL STAGE 4, THE CROWN): T1 RECONSTRUCT / T2 TRANSPLANT / T3 HUMAN-EDIT
#    -- GAP-SCAN + PRE-REGISTRATION (2026-07-06)".
# Brief: BABEL_PROGRAM_BRIEF_2026-07-05.md STAGE 4 (fired by _relay_l4.bat on _l3.done).
# MACHINERY reused VERBATIM: from _v7.py/_l3.py -- model loader / capture_h_all / proj_compl / s4_delta
#   named recon (b2P+q35P+y4) / folded-r48 recipe / frozen-rung forward / fkl / InjectHook additive
#   residual at BUS[b] / inject_kl_full / inject_kl_pidx ; from _l1.py -- the CH-WU token-image readout
#   (col=wte@(vdir*ln_f.weight); TOP40/BOT40 contrast) = the instrument that NAMED the axes.
# All tiers CONSUME the FROZEN ENCODER_V1 (_l3_encoder.pt 6be189567c41e91d); no weights are trained.
# T1 read->gloss->encode->substitute (39 cells, byte-replay decoder_v7 + frozen WELLPOSEDNESS_TABLE) ;
# T2 transplant A's gloss into B (gap-closure vs matched-random) ; T3 human-edit named axes, confusion
#   matrix vs matched-random edits (the crown). Standing decoder decoder_v7 (b1d2f464c00c3ef6).
import json, time, os, math, traceback, gc, subprocess, hashlib, ctypes
import torch, torch.nn as nn, torch.nn.functional as Fnn

t0=time.time()
DIR=r"C:\Shadow\Dissector\D0_PROGRAM\CONSTRUCTIVE"
SMOKE=os.environ.get("L4_SMOKE")=="1"
LOG=open(os.path.join(DIR,"_l4.log"),"a",encoding="utf-8")
def logln(s):
    s=str(s); LOG.write(f"[L4 {round(time.time()-t0,1):8.1f}s] "+s+"\n"); LOG.flush()
    try: print(s,flush=True)
    except Exception: pass
def el(): return round(time.time()-t0,1)
logln("="*100); logln(f"L4 START smoke={SMOKE} torch={torch.__version__}")
try:
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(),0x4000)
    logln("[ops] priority BelowNormal set")
except Exception as e: logln(f"[ops] priority set failed: {e}")
torch.set_num_threads(6)

# ---------------- locked constants (verbatim v7/l3) ----------------
EPS_KL=0.1871; CERT_BLOCK=512; IND_SEG=64; MB=4; CAP_CHUNK=16
VOCAB_SANS_SPECIALS=50256; REGIMES=["prose","code","repetition"]
FRESH_LO,FRESH_HI=24576,32768; REP_SEED=3
N_HOLD=16; TOL_REPLAY=2e-3
DEC_V7_SHA="b1d2f464c00c3ef6"; ENC_SHA="6be189567c41e91d"
N_NULLDIR=1 if SMOKE else 3
K_EDIT=[3,-3] if SMOKE else [3,-3,6,-6]        # +/-3 primary (antisym verdict), +/-6 report-only dose
SOFT_WALL_S=5*3600; HARD_WALL_S=int(11.5*3600)
# T3 edit magnitude sign convention: verdict antisym over the +/-3 pair; dose = +/-6.
FOLD_R48={("code",4),("code",5),("code",6),("code",7),("code",8),("code",9),("code",10),("code",11),
          ("prose",12),("repetition",8),("repetition",9),("repetition",10),("repetition",11),("repetition",12)}
RUNG_CELLS={("repetition",5):"surrogate",("repetition",6):"onset_b6",("repetition",7):"onset_b7"}
# 19-core field English names (LEXICON_V1 headers; carried in LEXICON_V3 Section 1)
FIELD_NAMES={0:"naval/warship",1:"collegiate-sports",2:"special-symbol<->temporal",3:"L0-magnitude/anomalous",
    4:"place-name<->statistics",5:"clause-final/physical-process",6:"epistemic-negative",7:"formula/markup-symbol",
    8:"harm/casualty",9:"sports-team",10:"punctuation-boundary",11:"coastal-storm/geography",12:"local-relation/admin",
    13:"quotation/boundary",14:"comma-boundary",15:"mixed-measurement",16:"spatial-preposition/@",17:"hyphen/@-format",
    18:"@-formatting"}

RESULT_JSON=os.path.join(DIR,"_l4_result_SMOKE.json" if SMOKE else "_l4_result.json")
BASES_PT=os.path.join(DIR,"_l4_bases_SMOKE.pt" if SMOKE else "_l4_bases.pt")
torch.manual_seed(1234)

PEN=("FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md :: 'L4 -- THE SPEAK TEST (BABEL STAGE 4, THE CROWN): "
     "T1 RECONSTRUCT / T2 TRANSPLANT / T3 HUMAN-EDIT -- GAP-SCAN + PRE-REGISTRATION (2026-07-06)'")
res={"experiment":"L4 speak test (Babel Stage 4): T1 reconstruct (read->gloss->encode->substitute, 39 "
     "cells vs recal floors + byte-replay), T2 transplant (encode context-A gloss into context-B, "
     "gap-closure vs matched-random), T3 human-edit (edit named axes, confusion matrix vs matched-random "
     "edits -- the crown). Consumes FROZEN ENCODER_V1. GPT-2 124M.",
     "date":"2026-07-06","propose_only":True,"pre_registration":PEN,
     "locked":{"tol_replay":TOL_REPLAY,"n_nulldir":N_NULLDIR,"k_edit":K_EDIT,
        "T1_bands":"COMPLETE==39 / MOSTLY 34-38 / BROKEN<34 (recal PRIMARY) ; bet COMPLETE80/MOSTLY15/BROKEN5",
        "T2_bands":"TRANSFER(sbar-null>=0.15 & sbar>0) / WEAK(0<margin<0.15) / NULL(margin<=0 or sbar<=0) ; "
                   "bet TRANSFER65/WEAK25/NULL10",
        "T3_bands":"per-family EDIT-CONTROLS-DIRECTION iff |Mii|>null95 & diag-dominant & sign-reproducible ; "
                   "N_ctrl of {naval,clause,rung}: STEERABLE>=2 / PARTIAL==1 / NULL==0 ; bet STEERABLE45/PARTIAL35/NULL20"},
     "config":{"n_hold":N_HOLD,"mb":MB,"cap_chunk":CAP_CHUNK,"cert_block":CERT_BLOCK,"ind_seg":IND_SEG,
        "precision":"fp32","tf32":"off","attn":"eager","seed":1234,"smoke":SMOKE},
     "gpu_free_checks":[],"instrument_discrepancy":[],"gates":{},
     "T1":{"cells":{},"demos":[]},"T2":{},"T3":{"confusion":{},"families":{}},"status":"INIT"}

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
        for k in ("T1","T2","T3","gates","gpu_free_checks","instrument_discrepancy"):
            if prev.get(k): res[k]=prev[k]
        logln(f"*** RESUME *** T1 cells={len(res['T1'].get('cells',{}))} T2={bool(res['T2'])} "
              f"T3fam={list(res['T3'].get('families',{}).keys())}")
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

# ---------------- model (v7 loader verbatim) ----------------
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

# ---------------- KL kernel + inject (v7 verbatim) ----------------
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
def inject_kl_pidx(ids_cpu,injhook,delta_full_g,Yclean,pidx):
    model=M["m"]; N=ids_cpu.shape[0]; tot=0.0; cnt=0; ci=0
    with torch.no_grad():
        for s0 in range(0,N,MB):
            s1=min(N,s0+MB)
            injhook.add=delta_full_g[s0:s1].to('cuda').float(); injhook.on=True
            lg=model(ids_cpu[s0:s1].to('cuda'),use_cache=False).logits; injhook.on=False; injhook.add=None
            kl=fkl(Yclean[ci].float()[:,pidx],lg.float()[:,pidx]); tot+=kl.sum().item(); cnt+=kl.numel(); ci+=1; del lg
    return tot/max(1,cnt)

# logits under a delta, plus CH-WU contrast on readouts + mean logit delta (for token-shift demos)
def logits_under_delta(ids_cpu,injhook,delta_full_g,readouts,pos_lo,pos_hi,Yclean=None,want_meanlogit=False):
    # readouts: list of (top_idx[40], bot_idx[40]) tensors on cuda. returns per-readout mean contrast over
    # positions [pos_lo,pos_hi) x blocks, plus optional mean-logit-delta vs Yclean (for token shifts).
    model=M["m"]; N=ids_cpu.shape[0]; nR=len(readouts)
    csum=[0.0]*nR; cnt=0; mlt=None
    if want_meanlogit: mlt=torch.zeros(M["wte"].shape[0],device='cuda'); mcnt=0
    with torch.no_grad():
        ci=0
        for s0 in range(0,N,MB):
            s1=min(N,s0+MB)
            if injhook is not None:
                injhook.add=delta_full_g[s0:s1].to('cuda').float(); injhook.on=True
            lg=model(ids_cpu[s0:s1].to('cuda'),use_cache=False).logits
            if injhook is not None: injhook.on=False; injhook.add=None
            lgp=lg[:,pos_lo:pos_hi,:].float()
            for ri,(top,bot) in enumerate(readouts):
                c=lgp[:,:,top].mean(-1)-lgp[:,:,bot].mean(-1); csum[ri]+=c.sum().item()
            cnt+=lgp.shape[0]*lgp.shape[1]
            if want_meanlogit and Yclean is not None:
                d=(lgp-Yclean[ci][:,pos_lo:pos_hi,:].float()); mlt+=d.reshape(-1,d.shape[-1]).sum(0); mcnt+=d.shape[0]*d.shape[1]
            ci+=1; del lg,lgp
    conts=[c/max(1,cnt) for c in csum]
    if want_meanlogit: return conts,(mlt/max(1,mcnt))
    return conts

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
    d=M["d"]; nL=M["nL"]; tok=M["tok"]; wte_g=M["wte"]; lnf_g=M["lnf"].to('cuda')

    # ---- GATE-0: hashes (encoder FROZEN + all sources) ----
    encsha=sha256(os.path.join(DIR,"_l3_encoder.pt"))
    d7sha=sha256(os.path.join(DIR,"decoder_v7_tensors.pt"))
    frecsha=sha256(os.path.join(DIR,"_v5_floors_recal.json"))
    lexsha=sha256(os.path.join(DIR,"LEXICON_V3.md"))
    mapsha=sha256(os.path.join(DIR,"_l2babel_maps.pt"))
    wpsha=sha256(os.path.join(DIR,"WELLPOSEDNESS_TABLE_V1.json"))
    ossha=sha256(os.path.join(DIR,"OFFSPAN_TABLE_V1.json"))
    grsha=sha256(os.path.join(DIR,"GRAMMAR_TABLE_V1.json"))
    enc_ok=(encsha==ENC_SHA); d7_ok=(d7sha==DEC_V7_SHA)
    res["gates"]["hashes"]={"encoder_v1":encsha,"encoder_ok":bool(enc_ok),"decoder_v7":d7sha,"decoder_v7_ok":bool(d7_ok),
        "floors_recal":frecsha,"lexicon_v3":lexsha,"l2babel_maps":mapsha,"wellposedness":wpsha,"offspan":ossha,"grammar":grsha}
    logln(f"[GATE-0] enc {encsha} ok={enc_ok} dec {d7sha} ok={d7_ok} wp {wpsha} floors {frecsha}")
    write_json()
    if (not enc_ok or not d7_ok) and not SMOKE:
        res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-A: encoder/decoder hash mismatch")

    # ---- load decoder_v7 objects (verbatim l3) ----
    D7=torch.load(os.path.join(DIR,"decoder_v7_tensors.pt"),map_location="cpu",weights_only=False)
    C=D7["C"].float(); B2=D7["B2"].float(); Q35=D7["Q35"].float(); Qu=D7["Q_union"].float()
    Qa=D7["Q_attn"].float(); Qm=D7["Q_mlp"].float(); hostQ=D7["host_Q"].float()
    mu=D7["mu"].float(); wteW=D7["wte_W"].float(); wtec=D7["wte_c"].float()
    read_W=D7["read_W"].float(); Vk=D7["m0_repera_Vk_recal"].float()
    # ---- load FROZEN ENCODER_V1 and CROSS-CHECK it equals decoder_v7's reader bases to machine precision
    ENC=torch.load(os.path.join(DIR,"_l3_encoder.pt"),map_location="cpu",weights_only=False)
    xcheck={}
    for nm,a,b in [("C",ENC["C"],C),("B2",ENC["B2"],B2),("Q35",ENC["Q35"],Q35),("Q_union",ENC["Q_union"],Qu),
                   ("mu",ENC["mu"],mu),("read_W",ENC["read_W"],read_W)]:
        xcheck[nm]=float((a.float()-b.float()).abs().max())
    enc_matches=all(v<=1e-6 for v in xcheck.values())
    res["gates"]["encoder_is_decoder_inverse"]={"max_abs_diff":xcheck,"pass":bool(enc_matches)}
    logln(f"[GATE-0b] ENCODER_V1 bases == decoder_v7 reader bases: {xcheck} -> {enc_matches}")
    C_g=C.to('cuda'); B2_g=B2.to('cuda'); Q35_g=Q35.to('cuda'); span5=torch.cat([B2_g,Q35_g],1)
    Qu_g=Qu.to('cuda'); Vk_g=Vk.to('cuda'); mu_g={b:mu[b].to('cuda') for b in range(nL+1)}
    wteW_g=wteW.to('cuda'); wtec_g=wtec.to('cuda')
    FOLD_O={}
    for b in range(4,12): FOLD_O[("code",b)]=D7[f"O_r48_code_b{b}"].float().to('cuda')
    FOLD_O[("prose",12)]=D7["O_r48_prose_b12"].float().to('cuda')
    for b in range(8,12): FOLD_O[("repetition",b)]=D7[f"O_r48_b{b}"].float().to('cuda')
    v5b=torch.load(os.path.join(DIR,"_v5_bases.pt"),map_location="cpu",weights_only=False)
    FOLD_O[("repetition",12)]=v5b["O_r48_b12"].float().to('cuda')
    O20_g={int(b):D7["O20"][b].float().to('cuda') for b in D7["O20"]}
    def load_rung(sd_key,scm_key,scs_key):
        r=LinearRung(1537,d).to('cuda').eval()
        r.load_state_dict({k:v.to('cuda').float() for k,v in D7[sd_key].items()})
        return r, D7[scm_key].to('cuda').float(), D7[scs_key].to('cuda').float()
    RUNG={}
    RUNG[("repetition",5)]=load_rung("surrogate_state_dict","surrogate_scaler_mean","surrogate_scaler_std")
    RUNG[("repetition",6)]=load_rung("onset_b6_state_dict","onset_b6_scaler_mean","onset_b6_scaler_std")
    RUNG[("repetition",7)]=load_rung("onset_b7_state_dict","onset_b7_scaler_mean","onset_b7_scaler_std")
    frec=json.load(open(os.path.join(DIR,"_v5_floors_recal.json"),encoding="utf-8"))
    floors_leg={int(b):{k:float(v) for k,v in frec["floors_legacy"][str(b)].items()} for b in range(13)}
    floors_rec={int(b):{k:(float(v) if v is not None else None) for k,v in frec["floors_recal"][str(b)].items()} for b in range(13)}
    RECAL_OK=(not frec.get("quarantined")) and frec.get("sg_early_ok") and frec.get("repl_all")
    v7rec=json.load(open(os.path.join(DIR,"_v7_result.json"),encoding="utf-8"))["verdict"]["tables"]["recal"]["cells"]
    def cell_bank(regime,b):
        c=v7rec.get(f"{regime}_b{b}"); return (float(c["KL"]) if c and c.get("KL") is not None else None)
    WPT=json.load(open(os.path.join(DIR,"WELLPOSEDNESS_TABLE_V1.json"),encoding="utf-8"))["cells"]
    def wpt_bank(regime,b):
        c=WPT.get(f"{regime}_b{b}"); return (float(c["KL"]) if c and c.get("KL") is not None else None)
    logln(f"[objects] loaded. RECAL_OK={RECAL_OK} r48={len(FOLD_O)} O20={len(O20_g)} rungs={len(RUNG)} WPT_cells={len(WPT)}")

    def proj_compl(x): return x-(x@span5)@span5.t()
    def wte_y4(ids_flat_g,b):
        Ecur=wte_g[ids_flat_g]; yhat=Ecur@wteW_g[b].t()+wtec_g[b]
        y2=yhat-(yhat@B2_g)@B2_g.t(); return y2-(y2@Q35_g)@Q35_g.t()
    # CH-WU token image (L1 verbatim): returns (top40, bot40) indices for a residual direction v.
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
    def get_regime(regime,need_wm0=False):
        if regime not in CAP:
            ids=build_regime_hold(regime); IDS[regime]=ids
            CAP[regime]=capture_h_all(ids,f"reg-{regime}",extra_wm0=(regime=="repetition"))
            YCL[regime]=clean_logits(ids)
        return IDS[regime],CAP[regime],YCL[regime]

    # rung reconstruction/edit feature builder (rep): feats=[x2,ecur,s]
    def rep_feats(ids,cap):
        x2=cap[2].to('cuda')-mu_g[2]; ecur=wte_g[ids.reshape(-1).to('cuda')]; s=cap['wm0'].to('cuda')@Vk_g
        return x2,ecur,s
    # recon at cell (regime,b) -- decoder_v7 grain (M2 recipe verbatim). returns recon [ntok,d].
    def recon_cell(regime,b,ids,cap,feats_full=None):
        Xc=cap[b].to('cuda')-mu_g[b]; ids_flat_g=ids.reshape(-1).to('cuda')
        b2P=(Xc@B2_g)@B2_g.t(); q35P=(Xc@Q35_g)@Q35_g.t(); y4=wte_y4(ids_flat_g,b)
        if (regime,b) in RUNG_CELLS:
            rung,scm,scs=RUNG[(regime,b)]
            with torch.no_grad(): oh=proj_compl(rung((feats_full-scm)/scs))
            return b2P+q35P+oh,"rung"
        elif (regime,b) in FOLD_O:
            O=FOLD_O[(regime,b)]; oP=(Xc@O)@O.t(); yk=y4-(y4@O)@O.t(); return b2P+q35P+oP+yk,"r48"
        elif b>=8 and b in O20_g:
            O=O20_g[b]; oP=(Xc@O)@O.t(); yk=y4-(y4@O)@O.t(); return b2P+q35P+oP+yk,"O20"
        else:
            return b2P+q35P+y4,"named"

    # ================= GATE-0 identity-inject exact-zero per regime =================
    id_regs=(["prose"] if SMOKE else REGIMES)
    id_sane=True; id_detail={}
    for regime in id_regs:
        ids,cap,Ycl=get_regime(regime,need_wm0=(regime=="repetition"))
        inj=InjectHook(M["blocks"][5])   # arbitrary boundary; identity delta is zero everywhere
        idkl,iddl=inject_kl_full(ids,inj,torch.zeros(ids.shape[0],CERT_BLOCK,d),Ycl,want_dl=True); inj.close()
        ok=bool(idkl<=1e-9 and iddl<=1e-4); id_sane=id_sane and ok
        id_detail[regime]={"kl":idkl,"dlogit":round(iddl,7),"pass":ok}
        logln(f"[GATE-0 identity {regime}] kl={idkl} dlogit={iddl} -> {ok}")
    res["gates"]["identity_inject"]={"detail":id_detail,"pass":bool(id_sane)}; write_json()
    if not id_sane and not SMOKE:
        res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-A: identity-inject not exact-zero")

    # ================= T1 -- RECONSTRUCT (read->gloss->encode->substitute, 39 cells) =================
    T1_PLAN=({"prose":[2,6,12],"code":[3,9],"repetition":[6,8]} if SMOKE else {r:list(range(nL+1)) for r in REGIMES})
    for regime in T1_PLAN:
        need=[b for b in T1_PLAN[regime] if f"{regime}_b{b}" not in res["T1"]["cells"]]
        if not need: logln(f"[T1 {regime}] all done skip"); continue
        gpu_free_check(f"T1-{regime}")
        ids,cap,Ycl=get_regime(regime,need_wm0=(regime=="repetition"))
        N=ids.shape[0]
        feats_full=None
        if regime=="repetition":
            x2,ecur,s=rep_feats(ids,cap); feats_full=torch.cat([x2,ecur,s],1)
        for b in T1_PLAN[regime]:
            key=f"{regime}_b{b}"
            if key in res["T1"]["cells"]: continue
            recon,kind=recon_cell(regime,b,ids,cap,feats_full)
            Xc=cap[b].to('cuda')-mu_g[b]
            delta=(recon-Xc).reshape(N,CERT_BLOCK,d)
            inj=InjectHook(M["blocks"][b-1]) if b>=1 else InjectHook(M["drop"])
            idkl,iddl=inject_kl_full(ids,inj,torch.zeros(N,CERT_BLOCK,d),Ycl,want_dl=True)
            if (regime,b) in RUNG_CELLS:
                meter="kl_rep"; dz=delta.clone(); dz[:, :IND_SEG, :]=0.0
                kl=inject_kl_pidx(ids,inj,dz,Ycl,torch.arange(IND_SEG,CERT_BLOCK))
            else:
                meter="kl_all"; kl=inject_kl_full(ids,inj,delta,Ycl)
            inj.close()
            fl_rec=floors_rec[b][regime] if floors_rec[b].get(regime) is not None else (0.1871 if regime=="prose" else None)
            fl_leg=floors_leg[b][regime]
            bank=cell_bank(regime,b); wbank=wpt_bank(regime,b)
            replay_ok=True; replay_d=None; wp_replay_ok=True; wp_replay_d=None
            if bank is not None:
                replay_d=abs(kl-bank); replay_ok=bool(replay_d<=TOL_REPLAY)
            if wbank is not None:
                wp_replay_d=abs(kl-wbank); wp_replay_ok=bool(wp_replay_d<=TOL_REPLAY)
            if not (replay_ok and wp_replay_ok):
                res["instrument_discrepancy"].append({"stage":f"T1-{key}","name":"byte_replay",
                    "why":f"kl={kl:.5f} v7bank={bank} wpbank={wbank} d7={replay_d} dwp={wp_replay_d}"})
            sane=bool(idkl<=1e-9 and iddl<=1e-4)
            rec_ok=bool(fl_rec is not None and kl<=fl_rec and sane and replay_ok and wp_replay_ok and RECAL_OK)
            res["T1"]["cells"][key]={"regime":regime,"b":b,"grain":kind,"meter":meter,"KL":round(kl,5),
                "floor_recal":fl_rec,"floor_legacy":fl_leg,"v7_bank":bank,"wp_bank":wbank,
                "replay_d":(round(replay_d,5) if replay_d is not None else None),
                "wp_replay_d":(round(wp_replay_d,5) if wp_replay_d is not None else None),
                "replay_ok":bool(replay_ok and wp_replay_ok),"identity_pass":sane,
                "reconstruct_ok":rec_ok,"legacy_pass":bool(kl<=fl_leg)}
            write_json()
            logln(f"[T1 {key}] {kind} KL={kl:.5f} recal={fl_rec} v7={bank} wp={wbank} replay_ok={replay_ok and wp_replay_ok} REC={rec_ok}")
        del feats_full; free()

    ncells=len(res["T1"]["cells"]); need_n=(7 if SMOKE else 39)
    if ncells>=need_n:
        cells=res["T1"]["cells"]; N_rec=sum(1 for k in cells if cells[k]["reconstruct_ok"])
        broken=[k for k in cells if not cells[k]["reconstruct_ok"]]
        replay_miss=[k for k in cells if not cells[k]["replay_ok"]]
        if SMOKE: verdict=("SMOKE-COMPLETE" if N_rec==ncells else "SMOKE-PARTIAL")
        else: verdict=("RECONSTRUCT-COMPLETE" if N_rec==39 else ("RECONSTRUCT-MOSTLY" if N_rec>=34 else "RECONSTRUCT-BROKEN"))
        res["T1"]["rollup"]={"n_cells":ncells,"N_rec":N_rec,"verdict":verdict,"broken_cells":broken,
            "replay_misses":replay_miss,"legacy_pass":sum(1 for k in cells if cells[k]["legacy_pass"]),
            "PASS":bool(verdict in ("RECONSTRUCT-COMPLETE","SMOKE-COMPLETE") and not replay_miss)}
        write_json(); logln(f"[T1 ROLLUP] N_rec={N_rec}/{ncells} -> {verdict} replay_misses={replay_miss}")

    # ---- T1 narrated demos (read a state -> ENGLISH -> re-encode -> KL inside floor) ----
    if not res["T1"].get("demos") or (SMOKE and len(res["T1"]["demos"])<1):
        # (regime,b,block,focus_field): focus_field selects the demo position (None=max total named-z);
        # positions < POS_MIN excluded (first-token outliers). Prose-b6 focuses field 0 (naval) so the
        # transcript pairs with the T3 naval-edit story.
        POS_MIN=32
        DEMOS=([("prose",6,7,0)] if SMOKE else
               [("prose",6,7,0),("prose",6,3,None),("code",9,5,None),("repetition",6,9,None),("prose",12,4,None)])
        demos=[]
        for (regime,b,blk,focus) in DEMOS:
            ids,cap,Ycl=get_regime(regime,need_wm0=(regime=="repetition"))
            key=f"{regime}_b{b}"; cellrec=res["T1"]["cells"].get(key,{})
            Hb=cap[b]; ntok=Hb.shape[0]
            base=blk*CERT_BLOCK
            xblk=(Hb[base:base+CERT_BLOCK].to('cuda')-mu_g[b])
            gcore=xblk@C_g                      # [512,19]
            gcore_sd=(cap[b].to('cuda')-mu_g[b])@C_g; sdv=gcore_sd.std(0).clamp(min=1e-6)
            if focus is not None: score=(gcore[:,focus].abs()/sdv[focus])
            else: score=(gcore.abs()/sdv).sum(1)
            score=score.clone(); score[:POS_MIN]=-1.0     # exclude first-token outliers
            pos=int(score.argmax())
            xp=xblk[pos]; gp=gcore[pos]
            zc=(gp/sdv)
            topf=torch.topk(zc.abs(),4).indices.tolist()
            named=[{"field":i,"name":FIELD_NAMES.get(i,f"f{i}"),"z":round(float(zc[i]),2)} for i in topf]
            gq=xp@Q35_g; zq=(gq/((cap[b].to('cuda')-mu_g[b])@Q35_g).std(0).clamp(min=1e-6))
            topq=torch.topk(zq.abs(),3).indices.tolist()
            corr=[{"corr_j":int(i),"z":round(float(zq[i]),2)} for i in topq]
            b2c=(xp@B2_g)@B2_g.t()             # content vector
            col=wte_g@(b2c/ (b2c.norm().clamp(min=1e-6)) *lnf_g)
            content_top=[tok.decode([int(i)]) for i in torch.topk(col,8).indices.tolist()]
            cur_tok=tok.decode([int(ids[blk,pos])])
            demos.append({"cell":key,"regime":regime,"b":b,"block":blk,"pos":pos,"current_token":cur_tok,
                "narration_named_fields":named,"narration_top_corridor":corr,"content_image_top_tokens":content_top,
                "reconstruct_KL":cellrec.get("KL"),"recal_floor":cellrec.get("floor_recal"),
                "inside_floor":cellrec.get("reconstruct_ok")})
            logln(f"[T1 demo {key} blk{blk} pos{pos}] cur='{cur_tok}' fields={[(n['name'],n['z']) for n in named]} KL={cellrec.get('KL')}")
        res["T1"]["demos"]=demos; write_json()

    # ================= T2 -- TRANSPLANT (encode A's gloss into B; gap-closure vs matched-random) =====
    if not res["T2"].get("done"):
        gpu_free_check("T2")
        b=6; regime="prose"
        ids,cap,Ycl=get_regime(regime); N=ids.shape[0]
        Xc=cap[b].to('cuda')-mu_g[b]; ids_flat_g=ids.reshape(-1).to('cuda')
        b2P=(Xc@B2_g)@B2_g.t(); q35P=(Xc@Q35_g)@Q35_g.t(); y4=wte_y4(ids_flat_g,b)
        recon_flat=(mu_g[b]+b2P+q35P+y4)          # [ntok,d] readable reconstruction (the encoded gloss)
        recon=recon_flat.reshape(N,CERT_BLOCK,d)
        Hb=cap[b].to('cuda').reshape(N,CERT_BLOCK,d)   # actual state (= mu+Xc)
        pairs=([(0,1),(2,3)] if SMOKE else [(i,(i+1)%N) for i in range(N)])
        inj=InjectHook(M["blocks"][b-1])
        gp=torch.Generator(device='cuda').manual_seed(20260706)
        per_pair=[]
        for (ai,bi) in pairs:
            # transplant delta at every position: recon_A - recon_B (swap readable content, keep B dark residual)
            dstate=(recon[ai]-recon[bi])                       # [512,d]
            deltaB=torch.zeros(N,CERT_BLOCK,d,device='cuda'); deltaB[bi]=dstate
            # clean A and B logits at all positions
            # p_A from Ycl[?]: Ycl is list by MB-chunk; recompute directly for the two blocks for clarity
            with torch.no_grad():
                lgA=M["m"](ids[ai:ai+1].to('cuda'),use_cache=False).logits[0].float()
                lgB=M["m"](ids[bi:bi+1].to('cuda'),use_cache=False).logits[0].float()
                inj.add=deltaB[bi:bi+1]; inj.on=True
                lgInj=M["m"](ids[bi:bi+1].to('cuda'),use_cache=False).logits[0].float(); inj.on=False; inj.add=None
            def klrow(pt,pp):  # KL(pt||pp) per position
                logpt=Fnn.log_softmax(pt,-1); p=logpt.exp(); logpp=Fnn.log_softmax(pp,-1)
                return (p*(logpt-logpp)).sum(-1)
            klBA=klrow(lgB,lgA).clamp(min=1e-9); klInjA=klrow(lgInj,lgA)
            s=((klBA-klInjA)/klBA)                              # gap-closure per position
            s_mean=float(s.mean())
            # matched-random null: random readable-subspace dir at matched per-position norm
            snull=[]
            for _ in range(N_NULLDIR):
                r=torch.randn(CERT_BLOCK,d,generator=gp,device='cuda'); r=(r@span5)@span5.t()   # into readable subspace
                r=r/ r.norm(dim=1,keepdim=True).clamp(min=1e-9) * dstate.norm(dim=1,keepdim=True)
                dn=torch.zeros(N,CERT_BLOCK,d,device='cuda'); dn[bi]=r
                with torch.no_grad():
                    inj.add=dn[bi:bi+1]; inj.on=True
                    lgN=M["m"](ids[bi:bi+1].to('cuda'),use_cache=False).logits[0].float(); inj.on=False; inj.add=None
                klNA=klrow(lgN,lgA); snull.append(float(((klBA-klNA)/klBA).mean()))
            per_pair.append({"A":ai,"B":bi,"s":round(s_mean,4),"s_null":round(sum(snull)/len(snull),4)})
        inj.close()
        sbar=sum(p["s"] for p in per_pair)/len(per_pair)
        sbar_null=sum(p["s_null"] for p in per_pair)/len(per_pair)
        import statistics as st
        se=(st.pstdev([p["s"] for p in per_pair])/math.sqrt(len(per_pair))) if len(per_pair)>1 else 0.0
        margin=sbar-sbar_null
        verdict=("TRANSFER" if (sbar>0 and margin>=0.15) else ("WEAK-TRANSFER" if margin>0 else "NULL"))
        res["T2"]={"done":True,"b":b,"regime":regime,"n_pairs":len(pairs),"sbar":round(sbar,4),
            "sbar_null":round(sbar_null,4),"margin":round(margin,4),"se":round(se,4),
            "verdict":verdict,"PASS":bool(verdict=="TRANSFER"),"per_pair":per_pair}
        write_json(); logln(f"[T2] sbar={sbar:.4f} null={sbar_null:.4f} margin={margin:.4f} -> {verdict}")
        # T2 demo: the pair with the largest transfer, with the top-token shift at the last position
        if not SMOKE:
            best=max(per_pair,key=lambda p:p["s"]); ai,bi=best["A"],best["B"]
            dstate=(recon[ai]-recon[bi]); deltaB=torch.zeros(N,CERT_BLOCK,d,device='cuda'); deltaB[bi]=dstate
            with torch.no_grad():
                lgB=M["m"](ids[bi:bi+1].to('cuda'),use_cache=False).logits[0].float()
                lgA=M["m"](ids[ai:ai+1].to('cuda'),use_cache=False).logits[0].float()
                inj2=InjectHook(M["blocks"][b-1]); inj2.add=deltaB[bi:bi+1]; inj2.on=True
                lgInj=M["m"](ids[bi:bi+1].to('cuda'),use_cache=False).logits[0].float(); inj2.on=False; inj2.close()
            pp=CERT_BLOCK-1
            Btop=[tok.decode([int(i)]) for i in torch.topk(lgB[pp],5).indices.tolist()]
            Atop=[tok.decode([int(i)]) for i in torch.topk(lgA[pp],5).indices.tolist()]
            Injtop=[tok.decode([int(i)]) for i in torch.topk(lgInj[pp],5).indices.tolist()]
            actxt=lambda blk: tok.decode([int(x) for x in ids[blk,max(0,pp-12):pp+1].tolist()])
            res["T2"]["demo"]={"A":ai,"B":bi,"s":best["s"],"pos":pp,
                "A_context_tail":actxt(ai),"B_context_tail":actxt(bi),
                "B_clean_top5":Btop,"A_clean_top5":Atop,"B_with_A_gloss_top5":Injtop}
            write_json(); logln(f"[T2 demo] B_clean={Btop} -> B+Agloss={Injtop} (A={Atop})")
        del Xc,b2P,q35P,y4,recon_flat,recon,Hb; free()

    # ================= T3 -- HUMAN-EDIT (the crown): confusion matrix vs matched-random edits =========
    if not res["T3"].get("done"):
        gpu_free_check("T3")
        # readout columns (CH-WU images), all axes -- computed once on cuda
        RD_DEFS=[("naval","proj",C_g[:,0],6,"prose"),
                 ("clause","proj",Q35_g[:,4],2,"prose"),
                 ("operator","proj",Q35_g[:,17],5,"code"),
                 ("symbol","proj",C_g[:,2],6,"prose"),
                 ("rung","rung",None,6,"repetition")]
        # rung readout image = mean onset-b6 output direction over rep holdout
        idsR,capR,YclR=get_regime("repetition",need_wm0=True)
        x2R,ecurR,sR=rep_feats(idsR,capR); featsR=torch.cat([x2R,ecurR,sR],1)
        rung6,scm6,scs6=RUNG[("repetition",6)]
        with torch.no_grad(): oh_realR=proj_compl(rung6((featsR-scm6)/scs6))
        rung_img_dir=oh_realR.mean(0); rung_img_dir=rung_img_dir/rung_img_dir.norm().clamp(min=1e-6)
        readouts=[]; rd_names=[]
        for (nm,kind,vec,bb,rg) in RD_DEFS:
            v=(vec if kind=="proj" else rung_img_dir); v=v/v.norm().clamp(min=1e-6)
            readouts.append(wu_image(v)); rd_names.append(nm)
        res["T3"]["readout_columns"]=rd_names; write_json()

        # edit families: required {naval,clause,rung} + control {operator}; matched-random null per family
        FAM=[("naval","proj",C_g[:,0],6,"prose","required"),
             ("clause","proj",Q35_g[:,4],2,"prose","required"),
             ("rung","rung",None,6,"repetition","required"),
             ("operator","proj",Q35_g[:,17],5,"code","control-manifold-bound")]
        if SMOKE: FAM=[FAM[0]]
        conf={}
        for (fnm,kind,vec,bb,rg,role) in FAM:
            if fnm in res["T3"].get("families",{}): continue
            ids,cap,Ycl=get_regime(rg,need_wm0=(rg=="repetition"))
            N=ids.shape[0]
            pos_lo,pos_hi=((IND_SEG,CERT_BLOCK) if rg=="repetition" else (0,CERT_BLOCK))
            inj=InjectHook(M["blocks"][bb-1]) if bb>=1 else InjectHook(M["drop"])
            # sigma of the edit axis coordinate over visited states
            if kind=="proj":
                v=vec/vec.norm().clamp(min=1e-6)
                coord=(cap[bb].to('cuda')-mu_g[bb])@v; sig=float(coord.std())
                def edit_delta(k):
                    dv=(k*sig)*v; return dv.view(1,1,d).expand(N,CERT_BLOCK,d).contiguous(), abs(k*sig)
            else:  # rung: push s feature, run forward, delta = oh(pushed)-oh(real)
                x2,ecur,s=rep_feats(ids,cap); feats=torch.cat([x2,ecur,s],1)
                rung,scm,scs=RUNG[(rg,bb)]
                with torch.no_grad(): oh_real=proj_compl(rung((feats-scm)/scs))
                sig=float(s.std())
                def edit_delta(k):
                    s2=s+k*sig; feats2=torch.cat([x2,ecur,s2],1)
                    with torch.no_grad(): ohp=proj_compl(rung((feats2-scm)/scs))
                    dv=(ohp-oh_real).reshape(N,CERT_BLOCK,d).contiguous()
                    mag=float(dv.reshape(-1,d).norm(dim=1).mean()); return dv, mag
            # clean contrasts (delta 0) with matched batching
            zero=torch.zeros(N,CERT_BLOCK,d,device='cuda')
            clean=logits_under_delta(ids,inj,zero,readouts,pos_lo,pos_hi)
            # per k, contrasts on ALL readouts + mean-logit-delta (for token shift on own readout)
            kc={}; ml={}
            for k in K_EDIT:
                dv,mag=edit_delta(k)
                if rg=="repetition": dv=dv.clone(); dv[:, :IND_SEG, :]=0.0
                cvals,mlt=logits_under_delta(ids,inj,dv,readouts,pos_lo,pos_hi,Yclean=Ycl,want_meanlogit=True)
                kc[k]=cvals; ml[k]=mlt
            # antisymmetric response over the +/-3 pair (verdict) and +/-6 (dose)
            def antisym(kp,km):
                return [ (kc[kp][j]-kc[km][j])/2.0 for j in range(len(readouts)) ]
            M3=antisym(3,-3); M6=(antisym(6,-6) if (6 in kc and -6 in kc) else None)
            own=rd_names.index(fnm) if fnm in rd_names else 0
            # matched-random-edit null on OWN readout (antisym over +/-3 with matched magnitude)
            _,mag3=edit_delta(3)
            gpn=torch.Generator(device='cuda').manual_seed(20260706+hash(fnm)%100000)
            nulls_own=[]
            for _ in range(N_NULLDIR):
                r=torch.randn(d,generator=gpn,device='cuda'); r=r/r.norm().clamp(min=1e-6)
                dvp=(mag3*r).view(1,1,d).expand(N,CERT_BLOCK,d).contiguous()
                dvm=(-mag3*r).view(1,1,d).expand(N,CERT_BLOCK,d).contiguous()
                if rg=="repetition":
                    dvp=dvp.clone(); dvp[:, :IND_SEG, :]=0.0; dvm=dvm.clone(); dvm[:, :IND_SEG, :]=0.0
                cp=logits_under_delta(ids,inj,dvp,[readouts[own]],pos_lo,pos_hi)[0]
                cm=logits_under_delta(ids,inj,dvm,[readouts[own]],pos_lo,pos_hi)[0]
                nulls_own.append(abs((cp-cm)/2.0))
            inj.close()
            null95=pct95(nulls_own)
            Mii=M3[own]; offdiag=[abs(M3[j]) for j in range(len(readouts)) if j!=own]
            diag_dom=bool(abs(Mii)>=max(offdiag)) if offdiag else True
            beats_null=bool(abs(Mii)>null95)
            sign_repro=bool(M6 is None or (Mii*M6[own]>0))
            controls=bool(beats_null and diag_dom and sign_repro)
            # token shift on own readout at the structured sign (sign of Mii): which English tokens rose
            k_show=3 if Mii>=0 else -3
            risers=[tok.decode([int(i)]) for i in torch.topk(ml[k_show],8).indices.tolist()]
            fallers=[tok.decode([int(i)]) for i in torch.topk(-ml[k_show],8).indices.tolist()]
            conf[fnm]={"role":role,"b":bb,"regime":rg,"sigma":round(sig,4),
                "M_row":{rd_names[j]:round(M3[j],4) for j in range(len(readouts))},
                "M6_row":({rd_names[j]:round(M6[j],4) for j in range(len(readouts))} if M6 else None),
                "own_readout":fnm,"Mii":round(Mii,4),"null95":round(null95,4),
                "diag_dominant":diag_dom,"beats_null":beats_null,"sign_reproducible":sign_repro,
                "EDIT_CONTROLS_DIRECTION":controls,"edit_sign_shown":k_show,
                "tokens_risen":risers,"tokens_fell":fallers}
            res["T3"].setdefault("families",{})[fnm]=conf[fnm]; write_json()
            logln(f"[T3 {fnm}] Mii={Mii:.4f} null95={null95:.4f} diagdom={diag_dom} beats={beats_null} "
                  f"signrepro={sign_repro} -> CONTROLS={controls} risen={risers[:5]}")
        # rollup over the 3 REQUIRED families
        fams=res["T3"]["families"]; req=["naval","clause","rung"]
        measurable=[f for f in req if f in fams]
        N_ctrl=sum(1 for f in measurable if fams[f]["EDIT_CONTROLS_DIRECTION"])
        control_fam=fams.get("operator")
        control_leaks=bool(control_fam and control_fam["EDIT_CONTROLS_DIRECTION"])
        if SMOKE: verdict="SMOKE-T3"
        else: verdict=("CROWN-STEERABLE" if N_ctrl>=2 else ("CROWN-PARTIAL" if N_ctrl==1 else "CROWN-NULL"))
        res["T3"]["rollup"]={"required":req,"measurable":measurable,"N_ctrl":N_ctrl,"verdict":verdict,
            "control_operator_controls":control_leaks,"PASS":bool(verdict=="CROWN-STEERABLE" and not control_leaks)}
        res["T3"]["done"]=True; write_json()
        logln(f"[T3 ROLLUP] N_ctrl={N_ctrl}/{len(measurable)} -> {verdict} control_leaks={control_leaks}")

    # ================= STATUS =================
    if SMOKE:
        t1ok=res["T1"].get("rollup",{}).get("verdict","")=="SMOKE-COMPLETE"
        anyreplay=any(res["T1"]["cells"][k]["v7_bank"] is not None for k in res["T1"]["cells"])
        res["status"]="SMOKE-"+("OK" if (t1ok and anyreplay and res["T2"].get("done") and res["T3"].get("done")) else "FAIL")
    else:
        done=(res["T1"].get("rollup") and len(res["T1"]["cells"])>=39 and res["T2"].get("done") and res["T3"].get("done"))
        res["status"]=("COMPLETE" if (done and not res["instrument_discrepancy"]) else
                       ("COMPLETE-WITH-DISCREPANCY" if done else "PARTIAL"))
    # freeze demo/table bases
    BASES["T1_rollup"]=res["T1"].get("rollup"); BASES["T2"]=res["T2"]; BASES["T3_rollup"]=res["T3"].get("rollup")
    save_bases(); write_json()
    if M["m"] is not None: del M["m"]; M["m"]=None; free()
except Exception as e:
    res["fatal_error"]={"error":str(e),"trace":traceback.format_exc()}
    logln(f"FATAL {e}\n{traceback.format_exc()}"); res.setdefault("status","FATAL")
write_json()
logln(f"L4 END status={res.get('status')} elapsed={el()}s T1cells={len(res['T1']['cells'])} "
      f"T2={res['T2'].get('verdict')} T3={res['T3'].get('rollup',{}).get('verdict')}")
open(os.path.join(DIR,"_l4_smoke_gpu.done" if SMOKE else "_l4_gpu.done"),"w").write(str(res.get("status","?"))+"\n")
logln("*** L4_"+("SMOKE_" if SMOKE else "")+"DONE ***"); LOG.flush(); LOG.close(); print("done")
