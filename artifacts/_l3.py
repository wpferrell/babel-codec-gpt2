# _l3.py -- L3 INVERSE MAPS (Babel Stage 3). PROPOSE-ONLY. GPT-2 124M.
# Pre-registration: FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md ::
#   "L3 -- INVERSE MAPS (BABEL STAGE 3): BUILD ENCODER_V1 ... PRE-REGISTRATION (2026-07-06)".
# Brief: BABEL_PROGRAM_BRIEF_2026-07-05.md STAGE 3 (fired by _relay_l3.bat on _l2_babel.done).
# MACHINERY reused VERBATIM from _v7.py (=_v6): model loader / capture / fkl / InjectHook /
#   inject_kl_full / inject_kl_pidx / proj_compl / s4_delta / folded-r48 recipe / frozen-rung forward /
#   substitution metering. THE ENCODER IS DEFINED, NOT TRAINED: every readable channel's gloss->state
#   map is the algebraic right-inverse of decoder_v7's frozen read. No optimization, no new weights.
# M1 GLOSS-EXACT (algebraic roundtrip) ; M2 WELLPOSED (39-cell encode-then-decode substitution KL vs
#   recal floors, per-cell byte-replay of decoder_v7's certified grain) ; M3 OFFSPAN (8 named axes,
#   sigma-matched nulls, extrapolation classification). Standing decoder decoder_v7 (b1d2f464c00c3ef6).
import json, time, os, math, traceback, gc, subprocess, hashlib, ctypes
import torch, torch.nn as nn, torch.nn.functional as Fnn

t0=time.time()
DIR=r"C:\Shadow\Dissector\D0_PROGRAM\CONSTRUCTIVE"
SMOKE=os.environ.get("L3_SMOKE")=="1"
LOG=open(os.path.join(DIR,"_l3.log"),"a",encoding="utf-8")
def logln(s):
    s=str(s); LOG.write(f"[L3 {round(time.time()-t0,1):8.1f}s] "+s+"\n"); LOG.flush()
    try: print(s,flush=True)
    except Exception: pass
def el(): return round(time.time()-t0,1)
logln("="*100); logln(f"L3 START smoke={SMOKE} torch={torch.__version__}")
try:
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(),0x4000)
    logln("[ops] priority BelowNormal set")
except Exception as e: logln(f"[ops] priority set failed: {e}")
torch.set_num_threads(6)

# ---------------- locked constants (verbatim v7) ----------------
EPS_KL=0.1871; CERT_BLOCK=512; IND_SEG=64; MB=4; CAP_CHUNK=16
VOCAB_SANS_SPECIALS=50256; REGIMES=["prose","code","repetition"]
FRESH_LO,FRESH_HI=24576,32768
REP_SEED=3; B2b=2; B5=5
N_HOLD=16                            # holdout blocks per regime (v7 fresh-window / rep SACRED size); smoke keeps full N so byte-replay is meaningful
TOL_REPLAY=2e-3
DEC_V7_SHA="b1d2f464c00c3ef6"
SOFT_WALL_S=3*3600; HARD_WALL_S=int(11.5*3600)
# decoder_v7's certified reconstruction grain per cell (V7 recal table is the authoritative KL bank).
# grain resolution priority: RUNG (rep b5/b6/b7) > r48 fold (FOLD_R48 cells) > O20 fold (b>=8) > named (S4).
FOLD_R48={("code",4),("code",5),("code",6),("code",7),("code",8),("code",9),("code",10),("code",11),
          ("prose",12),("repetition",8),("repetition",9),("repetition",10),("repetition",11),("repetition",12)}
RUNG_CELLS={("repetition",5):"surrogate",("repetition",6):"onset_b6",("repetition",7):"onset_b7"}
# M3 off-span axes (pre-registered; English names from LEXICON_V3). k grid + null dirs.
K_GRID=[3,5,10,-3,-5,-10] if not SMOKE else [5,-5]
N_NULLDIR=3 if not SMOKE else 1

RESULT_JSON=os.path.join(DIR,"_l3_result_SMOKE.json" if SMOKE else "_l3_result.json")
BASES_PT=os.path.join(DIR,"_l3_bases_SMOKE.pt" if SMOKE else "_l3_bases.pt")
ENCODER_PT=os.path.join(DIR,"_l3_encoder.pt")
ENCODER_JSON=os.path.join(DIR,"ENCODER_V1.json")
WP_JSON=os.path.join(DIR,"WELLPOSEDNESS_TABLE_V1.json")
OS_JSON=os.path.join(DIR,"OFFSPAN_TABLE_V1.json")
torch.manual_seed(1234)

PEN=("FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md :: 'L3 -- INVERSE MAPS (BABEL STAGE 3): BUILD ENCODER_V1 "
     "(gloss->state), WELL-POSEDNESS TABLE, OFF-SPAN BEHAVIOR -- GAP-SCAN + PRE-REGISTRATION (2026-07-06)'")
res={"experiment":"L3 inverse maps (Babel Stage 3): build+freeze ENCODER_V1 (gloss->state right-inverse "
     "of decoder_v7), well-posedness table (39-cell encode-then-decode substitution KL vs recal floors), "
     "off-span behavior (8 named axes, sigma-matched nulls). GPT-2 124M.",
     "date":"2026-07-06","propose_only":True,"pre_registration":PEN,
     "locked":{"eps_kl":EPS_KL,"tol_replay":TOL_REPLAY,
        "M1_bands":"EXACT<=1e-3 / APPROX<=1e-1 / LOSSY>1e-1 ; bet EXACT80/APPROX15/LOSSY5",
        "M2_bands":"WELL-POSED==39 / MOSTLY 34-38 / ILL<34 (recal PRIMARY) ; bet WP75/MOSTLY20/ILL5",
        "M3_bands":"per-axis STRUCTURED(mono&R>=1.5)/MANIFOLD-BOUND(1/1.5<R<1.5)/SATURATING ; "
                   "modal bet MANIFOLD50/STRUCTURED35/SATURATING15"},
     "config":{"n_hold":N_HOLD,"mb":MB,"cap_chunk":CAP_CHUNK,"cert_block":CERT_BLOCK,"ind_seg":IND_SEG,
        "precision":"fp32","tf32":"off","attn":"eager","seed":1234,"smoke":SMOKE,"k_grid":K_GRID,
        "n_nulldir":N_NULLDIR},
     "gpu_free_checks":[],"instrument_discrepancy":[],"gates":{},
     "M1":{},"M2":{"cells":{}},"M3":{"axes":{}},"encoder":{},"status":"INIT"}

def write_json():
    res["elapsed_s"]=el(); tmp=RESULT_JSON+".tmp"
    with open(tmp,"w",encoding="utf-8") as f: json.dump(res,f,indent=1)
    os.replace(tmp,RESULT_JSON)
BASES={}
def save_bases():
    tmp=BASES_PT+".tmp"; torch.save(BASES,tmp); os.replace(tmp,BASES_PT)

# ---------------- resume ----------------
if os.path.exists(RESULT_JSON):
    try:
        prev=json.load(open(RESULT_JSON,encoding="utf-8"))
        for k in ("M1","M2","M3","gates","gpu_free_checks","instrument_discrepancy","encoder"):
            if prev.get(k): res[k]=prev[k]
        logln(f"*** RESUME *** prior elapsed={prev.get('elapsed_s')} M2 cells={sorted(res['M2'].get('cells',{}).keys())}")
    except Exception as e: logln(f"resume load fail {e}")
if os.path.exists(BASES_PT):
    try: BASES=torch.load(BASES_PT,map_location="cpu",weights_only=False); logln(f"*** RESUME bases {len(BASES)}")
    except Exception as e: logln(f"bases load fail {e}"); BASES={}
write_json()

def sha256(path): return hashlib.sha256(open(path,"rb").read()).hexdigest()[:16]
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

# ---------------- captures ----------------
def capture_h_all(ids_cpu,tag,extra_wm0=False):
    model=M["m"]; nL=M["nL"]; N=ids_cpu.shape[0]; d=M["d"]; buf={}
    def mk(key):
        def h(mod,inp,out): buf[key]=(out[0] if isinstance(out,tuple) else out).detach()
        return h
    hh=[M["drop"].register_forward_hook(mk(0))]
    for L in range(nL): hh.append(M["blocks"][L].register_forward_hook(mk(L+1)))
    if extra_wm0: hh.append(M["blocks"][0].mlp.register_forward_hook(lambda m,i,o: buf.__setitem__('wm0',o.detach())))
    acc={b:[] for b in range(nL+1)};
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
    d=M["d"]; nL=M["nL"]
    # ---- GATE-0: hashes ----
    d7sha=sha256(os.path.join(DIR,"decoder_v7_tensors.pt"))
    frecsha=sha256(os.path.join(DIR,"_v5_floors_recal.json"))
    lexsha=sha256(os.path.join(DIR,"LEXICON_V3.md"))
    mapsha=sha256(os.path.join(DIR,"_l2babel_maps.pt"))
    d7_ok=(d7sha==DEC_V7_SHA)
    res["gates"]["hashes"]={"decoder_v7":d7sha,"decoder_v7_ok":bool(d7_ok),"floors_recal":frecsha,
                            "lexicon_v3":lexsha,"l2babel_maps":mapsha}
    if not d7_ok: res["instrument_discrepancy"].append({"stage":"gate0","name":"decoder_v7_hash","why":d7sha})
    logln(f"[GATE-0] decoder_v7 {d7sha} ok={d7_ok} floors {frecsha} lex {lexsha} maps {mapsha}")
    write_json()
    if not d7_ok and not SMOKE: res["status"]="GATE-FAIL"; write_json(); raise RuntimeError("FB-A: decoder_v7 hash")

    # ---- load decoder_v7 objects ----
    D7=torch.load(os.path.join(DIR,"decoder_v7_tensors.pt"),map_location="cpu",weights_only=False)
    C=D7["C"].float(); B2=D7["B2"].float(); Q35=D7["Q35"].float(); Qu=D7["Q_union"].float()
    Qa=D7["Q_attn"].float(); Qm=D7["Q_mlp"].float(); hostQ=D7["host_Q"].float()
    mu=D7["mu"].float(); wteW=D7["wte_W"].float(); wtec=D7["wte_c"].float()
    read_W=D7["read_W"].float(); read_c=D7["read_c"].float()
    Vk=D7["m0_repera_Vk_recal"].float()
    C_g=C.to('cuda'); B2_g=B2.to('cuda'); Q35_g=Q35.to('cuda'); span5=torch.cat([B2_g,Q35_g],1)
    Qu_g=Qu.to('cuda'); Vk_g=Vk.to('cuda'); mu_g={b:mu[b].to('cuda') for b in range(nL+1)}
    wteW_g=wteW.to('cuda'); wtec_g=wtec.to('cuda'); wte_g=M["wte"]
    # fold bases
    FOLD_O={}
    for b in range(4,12): FOLD_O[("code",b)]=D7[f"O_r48_code_b{b}"].float().to('cuda')
    FOLD_O[("prose",12)]=D7["O_r48_prose_b12"].float().to('cuda')
    for b in range(8,12): FOLD_O[("repetition",b)]=D7[f"O_r48_b{b}"].float().to('cuda')
    v5b=torch.load(os.path.join(DIR,"_v5_bases.pt"),map_location="cpu",weights_only=False)
    FOLD_O[("repetition",12)]=v5b["O_r48_b12"].float().to('cuda')
    # O20 late folds (V3 S7 grain; boundary-keyed 8..12) -> used at prose b8..b11 and code b12
    O20_g={int(b):D7["O20"][b].float().to('cuda') for b in D7["O20"]}
    # rungs
    def load_rung(sd_key,sc_mean_key,sc_std_key):
        r=LinearRung(1537,d).to('cuda').eval()
        r.load_state_dict({k:v.to('cuda').float() for k,v in D7[sd_key].items()})
        return r, D7[sc_mean_key].to('cuda').float(), D7[sc_std_key].to('cuda').float()
    RUNG={}
    RUNG[("repetition",5)]=load_rung("surrogate_state_dict","surrogate_scaler_mean","surrogate_scaler_std")
    RUNG[("repetition",6)]=load_rung("onset_b6_state_dict","onset_b6_scaler_mean","onset_b6_scaler_std")
    RUNG[("repetition",7)]=load_rung("onset_b7_state_dict","onset_b7_scaler_mean","onset_b7_scaler_std")
    # floors
    frec=json.load(open(os.path.join(DIR,"_v5_floors_recal.json"),encoding="utf-8"))
    floors_leg={int(b):{k:float(v) for k,v in frec["floors_legacy"][str(b)].items()} for b in range(13)}
    floors_rec={int(b):{k:(float(v) if v is not None else None) for k,v in frec["floors_recal"][str(b)].items()} for b in range(13)}
    RECAL_OK=(not frec.get("quarantined")) and frec.get("sg_early_ok") and frec.get("repl_all")
    v3=json.load(open(os.path.join(DIR,"_v3_result.json"),encoding="utf-8")); v3cells=v3["cells"]
    # V7 recal table = authoritative decoder_v7 certified per-cell KL bank (byte-replay target, all 39)
    v7rec=json.load(open(os.path.join(DIR,"_v7_result.json"),encoding="utf-8"))["verdict"]["tables"]["recal"]["cells"]
    def cell_bank(regime,b):
        c=v7rec.get(f"{regime}_b{b}"); return (float(c["KL"]) if c and c.get("KL") is not None else None)
    logln(f"[objects] loaded. RECAL_OK={RECAL_OK} r48_folds={len(FOLD_O)} O20_folds={len(O20_g)} rungs={len(RUNG)}")

    def proj_compl(x): return x-(x@span5)@span5.t()
    def wte_y4(ids_flat_g,b):
        Ecur=wte_g[ids_flat_g]; yhat=Ecur@wteW_g[b].t()+wtec_g[b]
        y2=yhat-(yhat@B2_g)@B2_g.t(); return y2-(y2@Q35_g)@Q35_g.t()

    # ======================= ENCODER_V1 build (right-inverse operators) =======================
    # projection channels: encode = basis @ coords (orthonormal -> pinv = transpose); read_W right-inverse.
    def right_pinv(W):  # W [k,p], right inverse [p,k] s.t. W @ pinv = I_k
        return W.t()@torch.linalg.inv(W@W.t()+1e-9*torch.eye(W.shape[0]))
    readW_pinv=torch.stack([right_pinv(read_W[b]) for b in range(read_W.shape[0])])  # [13,385,19]
    res["encoder"]={"channels":{
        "core_C":{"encode":"dh = C @ g (g in R^19)","shape":list(C.shape),"orthonormal":True},
        "corridor_Q35":{"encode":"dh = Q35 @ g (g in R^35)","shape":list(Q35.shape),"orthonormal":True},
        "content_B2":{"encode":"dh = B2 @ g (g in R^404)","shape":list(B2.shape),"orthonormal":True},
        "door_Q_union":{"encode":"dh = Q_union @ c (c in R^385 door coords)","shape":list(Qu.shape)},
        "door_read19":{"encode":"c = readW_pinv[b] @ g19 ; dh = Q_union @ c","shape":list(read_W.shape),
                       "note":"read_W[b] 19<-385 summarizer right-inverse"},
        "door_Q_attn":{"encode":"dh = Q_attn @ c","shape":list(Qa.shape)},
        "door_Q_mlp":{"encode":"dh = Q_mlp @ c","shape":list(Qm.shape)},
        "wte":{"encode":"by construction: y4(token,b)=proj_compl(wte[tok]@wteW[b]^T+wtec[b])","note":"deterministic in token"},
        "fold_O_r48":{"encode":"dh = O_r48_cell @ f (per cell)","cells":sorted([f"{r}_b{b}" for (r,b) in FOLD_O])},
        "rung":{"encode":"run forward: oh=proj_compl(rung((feats-mean)/std)) ; feats=[x2,ecur,s]",
                "cells":sorted([f"{r}_b{b}" for (r,b) in RUNG])},
        "seam_operators":{"source":"_l2babel_maps.pt (frozen)","sha":mapsha,
                          "note":"W_regime_b [19,19]+bias -- seam-to-seam law for L4 T1 (referenced, not rebuilt)"}}}
    write_json()

    # ======================= M1 -- GLOSS-EXACT (algebraic roundtrip) =======================
    if not res["M1"].get("done"):
        gpu_free_check("M1")
        # capture a prose holdout to get real states for the roundtrip (mid boundary b6)
        WIKI=M["tok"](load_wiki_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
        ids_pr=ids_window(WIKI,FRESH_LO,FRESH_LO+N_HOLD*CERT_BLOCK,"wiki M1")
        cap=capture_h_all(ids_pr,"M1-prose")
        def roundtrip(basis_g,b):
            x=(cap[b].to('cuda')-mu_g[b]); g=x@basis_g
            num=((g@basis_g.t())@basis_g - g)  # (B^T B - I) g
            rel=(num.norm(dim=1)/g.norm(dim=1).clamp(min=1e-9))
            return float(rel.max()), float((basis_g.t()@basis_g-torch.eye(basis_g.shape[1],device='cuda')).norm())
        chans={"core_C":(C_g,6),"content_B2":(B2_g,6),"corridor_Q35":(Q35_g,2),
               "door_Q_union":(Qu_g,6),"door_Q_attn":(Qa.to('cuda'),6),"door_Q_mlp":(Qm.to('cuda'),6),
               "host_Q":(hostQ.to('cuda'),6)}
        m1={}
        for nm,(bg,b) in chans.items():
            r,orth=roundtrip(bg,b); m1[nm]={"roundtrip_rel_max":r,"orth_resid":orth,
                "band":("EXACT" if r<=1e-3 else ("APPROX" if r<=1e-1 else "LOSSY"))}
            logln(f"[M1 {nm}] roundtrip={r:.3e} orth={orth:.3e} -> {m1[nm]['band']}")
        # fold bases roundtrip (per cell, at cell boundary; use prose cap boundary as proxy for shape only)
        fold_rt=[]
        for (rg,b),O in FOLD_O.items():
            x=(cap[min(b,12)].to('cuda')-mu_g[min(b,12)]); g=x@O
            num=((g@O.t())@O-g); rel=float((num.norm(dim=1)/g.norm(dim=1).clamp(min=1e-9)).max())
            fold_rt.append(rel)
        m1["fold_O_r48_max"]={"roundtrip_rel_max":max(fold_rt),"n_cells":len(fold_rt),
            "band":("EXACT" if max(fold_rt)<=1e-3 else ("APPROX" if max(fold_rt)<=1e-1 else "LOSSY"))}
        # read_W right-inverse residual per boundary
        rw_res=[]
        for b in range(read_W.shape[0]):
            resid=float((read_W[b]@readW_pinv[b]-torch.eye(19)).norm()); rw_res.append(resid)
        m1["door_read19_rightinv"]={"resid_max":max(rw_res),"resid_per_b":[round(x,5) for x in rw_res],
            "band":("EXACT" if max(rw_res)<=1e-3 else ("APPROX" if max(rw_res)<=1e-1 else "LOSSY"))}
        proj_bands=[m1[k]["band"] for k in m1 if k!="door_read19_rightinv"]
        worst=max([m1[k]["roundtrip_rel_max"] for k in m1 if k!="door_read19_rightinv"])
        verdict=("EXACT" if worst<=1e-3 else ("APPROX" if worst<=1e-1 else "LOSSY"))
        m1["VERDICT"]={"max_roundtrip_projection":worst,"H_L3_GLOSS_EXACT":verdict,
            "bet_favorite_hit":bool(verdict=="EXACT")}
        m1["done"]=True; res["M1"]=m1; write_json()
        del cap; free()
        logln(f"[M1 VERDICT] worst={worst:.3e} -> {verdict}")

    # ======================= M2 -- WELLPOSED (39-cell encode-then-decode) =======================
    def build_regime_hold(regime):
        if regime=="prose":
            WIKI=M["tok"](load_wiki_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
            return ids_window(WIKI,FRESH_LO,FRESH_LO+N_HOLD*CERT_BLOCK,"wiki hold")
        if regime=="code":
            CIDS=M["tok"](load_code_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
            return ids_window(CIDS,FRESH_LO,FRESH_LO+N_HOLD*CERT_BLOCK,"code hold")
        if regime=="repetition":
            return build_dind(N_HOLD,CERT_BLOCK,REP_SEED)
        raise RuntimeError(regime)

    # SMOKE exercises every grain type: prose named(b2)/O20(b11)/r48(b12); code named(b3)/O20(b12); rep rung(b6)/r48(b8)
    PLAN=({"prose":[2,11,12],"code":[3,12],"repetition":[6,8]} if SMOKE else {r:list(range(nL+1)) for r in REGIMES})
    for regime in PLAN:
        plan_bs=PLAN[regime]
        need=[b for b in plan_bs if f"{regime}_b{b}" not in res["M2"]["cells"]]
        if not need: logln(f"[M2 {regime}] all done skip"); continue
        if el()>HARD_WALL_S: break
        gpu_free_check(f"M2-{regime}")
        ids=build_regime_hold(regime); N=ids.shape[0]
        cap=capture_h_all(ids,f"M2-{regime}",extra_wm0=(regime=="repetition"))
        Ycl=clean_logits(ids)
        ids_flat_g=ids.reshape(-1).to('cuda')
        # rung features (rep only): x2,ecur,s
        if regime=="repetition":
            x2=cap[2].to('cuda')-mu_g[2]; ecur=wte_g[ids_flat_g]; s=cap['wm0'].to('cuda')@Vk_g
            feats_full=torch.cat([x2,ecur,s],1)   # [ntok,1537]
        for b in plan_bs:
            key=f"{regime}_b{b}"
            if key in res["M2"]["cells"]: continue
            if el()>HARD_WALL_S: break
            Xc=cap[b].to('cuda')-mu_g[b]
            b2P=(Xc@B2_g)@B2_g.t(); q35P=(Xc@Q35_g)@Q35_g.t()
            y4=wte_y4(ids_flat_g,b)
            bank=cell_bank(regime,b)   # decoder_v7 certified KL (V7 recal table) -- authoritative
            # grain resolution: rung > r48 fold > O20 fold (b>=8) > named
            if (regime,b) in RUNG_CELLS:
                cell_kind="rung"; rung,scm,scs=RUNG[(regime,b)]
                with torch.no_grad(): oh=proj_compl(rung((feats_full-scm)/scs))
                recon=b2P+q35P+oh
            elif (regime,b) in FOLD_O:
                cell_kind="r48"; O=FOLD_O[(regime,b)]
                oP=(Xc@O)@O.t(); yk=y4-(y4@O)@O.t(); recon=b2P+q35P+oP+yk
            elif b>=8 and b in O20_g:
                cell_kind="O20"; O=O20_g[b]
                oP=(Xc@O)@O.t(); yk=y4-(y4@O)@O.t(); recon=b2P+q35P+oP+yk
            else:
                cell_kind="named"; recon=b2P+q35P+y4
            delta=(recon-Xc).reshape(N,CERT_BLOCK,d)
            inj=InjectHook(M["blocks"][b-1]) if b>=1 else InjectHook(M["drop"])
            # identity sanity
            id_kl,id_dl=inject_kl_full(ids,inj,torch.zeros(N,CERT_BLOCK,d),Ycl,want_dl=True)
            # metering (verbatim decoder_v7 grain): rung cells kl_rep (IND_SEG zeroed, [64,512)); ALL else kl_all
            if (regime,b) in RUNG_CELLS:
                meter="kl_rep"; dz=delta.clone(); dz[:, :IND_SEG, :]=0.0
                kl=inject_kl_pidx(ids,inj,dz,Ycl,torch.arange(IND_SEG,CERT_BLOCK))
            else:
                meter="kl_all"; kl=inject_kl_full(ids,inj,delta,Ycl)
            inj.close()
            fl_rec=floors_rec[b][regime] if floors_rec[b].get(regime) is not None else (0.1871 if regime=="prose" else None)
            fl_leg=floors_leg[b][regime]
            replay_ok=True; replay_d=None
            if bank is not None:
                replay_d=abs(kl-bank); replay_ok=bool(replay_d<=TOL_REPLAY)
                if not replay_ok:
                    res["instrument_discrepancy"].append({"stage":f"M2-{key}","name":"byte_replay",
                        "why":f"kl={kl:.5f} bank={bank} d={replay_d:.5f}"})
            sane=bool(id_kl<=1e-9 and id_dl<=1e-4)
            if not sane:
                res["instrument_discrepancy"].append({"stage":f"M2-{key}","name":"identity","why":f"kl={id_kl} dl={id_dl}"})
            wp=bool(fl_rec is not None and kl<=fl_rec and sane and replay_ok and RECAL_OK)
            res["M2"]["cells"][key]={"regime":regime,"b":b,"grain":cell_kind,"meter":meter,"KL":round(kl,5),
                "floor_recal":fl_rec,"floor_legacy":fl_leg,"bank":bank,"replay_d":(round(replay_d,5) if replay_d is not None else None),
                "replay_ok":replay_ok,"identity_kl":id_kl,"identity_dlogit":round(id_dl,6),"identity_pass":sane,
                "well_posed":wp,"legacy_pass":bool(kl<=fl_leg)}
            write_json()
            logln(f"[M2 {key}] {cell_kind} KL={kl:.5f} recal={fl_rec} bank={bank} replay_ok={replay_ok} WP={wp}")
        del cap,Ycl; free()
        if regime=="repetition":
            try: del feats_full,x2,ecur,s
            except Exception: pass
            free()

    # M2 rollup
    if len(res["M2"]["cells"])>=(2 if SMOKE else 39):
        cells=res["M2"]["cells"]; N_wp=sum(1 for k in cells if cells[k]["well_posed"])
        ntot=len(cells)
        illposed=[k for k in cells if not cells[k]["well_posed"]]
        verdict=("WELL-POSED" if N_wp==ntot else ("MOSTLY-WELL-POSED" if N_wp>=ntot-5 else "ILL-POSED"))
        replay_misses=[k for k in cells if not cells[k]["replay_ok"]]
        res["M2"]["rollup"]={"n_cells":ntot,"N_wp":N_wp,"H_L3_WELLPOSED":verdict,
            "bet_favorite_hit":bool(verdict=="WELL-POSED"),"illposed_cells":illposed,
            "replay_misses":replay_misses,"legacy_pass":sum(1 for k in cells if cells[k]["legacy_pass"])}
        write_json()
        logln(f"[M2 ROLLUP] N_wp={N_wp}/{ntot} -> {verdict} replay_misses={replay_misses}")

    # ======================= M3 -- OFFSPAN (8 named axes) =======================
    AXES=[
        {"id":"core_dim0_naval","kind":"proj","vec":C[:,0],"b":6,"regime":"prose","name":"core dim0 naval/warship"},
        {"id":"core_dim2_symbol","kind":"proj","vec":C[:,2],"b":6,"regime":"prose","name":"core dim2 special-symbol<->temporal"},
        {"id":"corr_j4_clause","kind":"proj","vec":Q35[:,4],"b":2,"regime":"prose","name":"corr_j4 clause/delimiter-boundary (b2_d4)"},
        {"id":"corr_j17_operator","kind":"proj","vec":Q35[:,17],"b":5,"regime":"code","name":"corr_j17 operator/keyword-anchor (b5_d5)"},
        {"id":"door_qattn_top","kind":"proj","vec":Qa[:,0],"b":6,"regime":"prose","name":"door Q_attn top-variance"},
        {"id":"fold_b12_d45_corp","kind":"proj","vec":None,"b":12,"regime":"prose","name":"fold O_r48_b12_d45 corporate-name-tail"},
        {"id":"rung_repb6_onset","kind":"rung","b":6,"regime":"repetition","name":"rep_b6 onset rung input push (run forward)"},
        {"id":"glitch_j0_DEAF","kind":"proj","vec":Q35[:,0],"b":2,"regime":"prose","name":"glitch axis b2_d0 (LEXICON DEAF control)"},
    ]
    l1b=torch.load(os.path.join(DIR,"_l1_bases.pt"),map_location="cpu",weights_only=False)
    if "vec_fold_O_r48_b12_d45" in l1b: AXES[5]["vec"]=l1b["vec_fold_O_r48_b12_d45"].float()
    else: AXES[5]["vec"]=FOLD_O[("repetition",12)][:,45].cpu()
    for _i,_ax in enumerate(AXES): _ax["seed"]=20260706+_i*101   # deterministic per-axis null seed (resume-safe)
    if SMOKE: AXES=[AXES[0],AXES[7]]

    cap_by={}  # (regime) -> capture
    def get_cap_m3(regime):
        if regime not in cap_by:
            ids=build_regime_hold(regime)
            cap_by[regime]={"ids":ids,"cap":capture_h_all(ids,f"M3-{regime}",extra_wm0=(regime=="repetition")),
                            "Ycl":clean_logits(ids)}
        return cap_by[regime]

    for ax in AXES:
        if ax["id"] in res["M3"]["axes"]: continue
        if el()>SOFT_WALL_S and ax["id"]!="glitch_j0_DEAF":
            res["M3"]["axes"][ax["id"]]={"DROPPED":"budget wall"}; write_json(); continue
        cm=get_cap_m3(ax["regime"]); ids=cm["ids"]; cap=cm["cap"]; Ycl=cm["Ycl"]; N=ids.shape[0]
        b=ax["b"]; inj=InjectHook(M["blocks"][b-1]) if b>=1 else InjectHook(M["drop"])
        gp=torch.Generator(device='cuda').manual_seed(ax["seed"])
        rows={}
        if ax["kind"]=="proj":
            vec=ax["vec"].to('cuda'); vec=vec/vec.norm()
            Xc=cap[b].to('cuda')-mu_g[b]; coord=Xc@vec
            mu_c=float(coord.mean()); sd_c=float(coord.std())
            # sigma-matched null dirs (orthogonal to vec)
            nulls=[]
            for _ in range(N_NULLDIR):
                r=torch.randn(d,generator=gp,device='cuda'); r=r-(r@vec)*vec; r=r/r.norm(); nulls.append(r)
            for k in K_GRID:
                mag=abs(k*sd_c)
                dvec=(k*sd_c)*vec
                delta=dvec.view(1,1,d).expand(N,CERT_BLOCK,d)
                if ax["regime"]=="repetition":
                    dz=delta.clone(); dz[:, :IND_SEG, :]=0.0
                    kl_ax=inject_kl_pidx(ids,inj,dz,Ycl,torch.arange(IND_SEG,CERT_BLOCK))
                else:
                    kl_ax=inject_kl_full(ids,inj,delta,Ycl)
                kl_nulls=[]
                for r in nulls:
                    dn=(mag*r).view(1,1,d).expand(N,CERT_BLOCK,d)
                    if ax["regime"]=="repetition":
                        dz=dn.clone(); dz[:, :IND_SEG, :]=0.0
                        kl_nulls.append(inject_kl_pidx(ids,inj,dz,Ycl,torch.arange(IND_SEG,CERT_BLOCK)))
                    else:
                        kl_nulls.append(inject_kl_full(ids,inj,dn,Ycl))
                kl_null=sum(kl_nulls)/len(kl_nulls)
                rows[str(k)]={"kl_axis":round(kl_ax,5),"kl_null":round(kl_null,5),
                              "R":round(kl_ax/max(kl_null,1e-9),4),"mag":round(mag,4)}
                logln(f"[M3 {ax['id']} k={k}] KLax={kl_ax:.5f} KLnull={kl_null:.5f} R={rows[str(k)]['R']}")
        else:  # rung: push the s scalar off-span, run forward
            x2=cap[2].to('cuda')-mu_g[2]; ecur=wte_g[ids.reshape(-1).to('cuda')]; s=cap['wm0'].to('cuda')@Vk_g
            rung,scm,scs=RUNG[(ax["regime"],b)]
            with torch.no_grad(): oh_real=proj_compl(rung((torch.cat([x2,ecur,s],1)-scm)/scs))
            sd_s=float(s.std()); obj_real=proj_compl(cap[b].to('cuda')-mu_g[b])
            # null: random unit dirs in state space at matched magnitude
            nulls=[]
            for _ in range(N_NULLDIR):
                r=torch.randn(d,generator=gp,device='cuda'); r=r/r.norm(); nulls.append(r)
            for k in K_GRID:
                s2=s+k*sd_s
                with torch.no_grad(): oh_push=proj_compl(rung((torch.cat([x2,ecur,s2],1)-scm)/scs))
                dvec=(oh_push-oh_real).reshape(N,CERT_BLOCK,d); mag=float(dvec.reshape(-1,d).norm(dim=1).mean())
                dz=dvec.clone(); dz[:, :IND_SEG, :]=0.0
                kl_ax=inject_kl_pidx(ids,inj,dz,Ycl,torch.arange(IND_SEG,CERT_BLOCK))
                kl_nulls=[]
                for r in nulls:
                    dn=(mag*r).view(1,1,d).expand(N,CERT_BLOCK,d)
                    dz2=dn.clone(); dz2[:, :IND_SEG, :]=0.0
                    kl_nulls.append(inject_kl_pidx(ids,inj,dz2,Ycl,torch.arange(IND_SEG,CERT_BLOCK)))
                kl_null=sum(kl_nulls)/len(kl_nulls)
                rows[str(k)]={"kl_axis":round(kl_ax,5),"kl_null":round(kl_null,5),
                              "R":round(kl_ax/max(kl_null,1e-9),4),"mag":round(mag,4)}
                logln(f"[M3 {ax['id']} k={k}] KLax={kl_ax:.5f} KLnull={kl_null:.5f} R={rows[str(k)]['R']}")
        inj.close(); free()
        # classification: R at |k|=10 (mean of +10,-10), monotone in |k|
        def klat(kk): return rows.get(str(kk),{}).get("kl_axis",0.0)
        R10=None
        if "10" in rows and "-10" in rows:
            R10=(rows["10"]["R"]+rows["-10"]["R"])/2
        elif rows: R10=list(rows.values())[-1]["R"]
        pos_mono=all(klat(3)<=klat(5)<=klat(10) for _ in [0]) if all(str(x) in rows for x in (3,5,10)) else None
        cls=("STRUCTURED-EXTRAPOLATION" if (R10 is not None and R10>=1.5) else
             ("MANIFOLD-BOUND" if (R10 is not None and R10>1/1.5) else "SATURATING-OR-NULL"))
        res["M3"]["axes"][ax["id"]]={"name":ax["name"],"b":b,"regime":ax["regime"],"kind":ax["kind"],
            "rows":rows,"R_k10":(round(R10,4) if R10 is not None else None),"pos_monotone":pos_mono,"class":cls}
        write_json()
        logln(f"[M3 {ax['id']}] R(|k|=10)={R10} -> {cls}")

    # M3 rollup
    axcls=[v["class"] for v in res["M3"]["axes"].values() if isinstance(v,dict) and v.get("class")]
    if axcls:
        from collections import Counter
        modal=Counter(axcls).most_common(1)[0][0]
        res["M3"]["rollup"]={"n_axes":len(axcls),"classes":dict(Counter(axcls)),"modal_class":modal,
            "bet_favorite_hit":bool(modal=="MANIFOLD-BOUND")}
        write_json(); logln(f"[M3 ROLLUP] modal={modal} {dict(Counter(axcls))}")

    # ======================= FREEZE ENCODER_V1 =======================
    if not SMOKE and res["M1"].get("done") and len(res["M2"]["cells"])>=39:
        ENC={"C":C.contiguous(),"B2":B2.contiguous(),"Q35":Q35.contiguous(),"Q_union":Qu.contiguous(),
             "Q_attn":Qa.contiguous(),"Q_mlp":Qm.contiguous(),"host_Q":hostQ.contiguous(),
             "read_W":read_W.contiguous(),"read_W_pinv":readW_pinv.contiguous(),
             "wte_W":wteW.contiguous(),"wte_c":wtec.contiguous(),"mu":mu.contiguous(),"Vk":Vk.contiguous(),
             "span5_cols":[B2.shape[1],Q35.shape[1]]}
        for (rg,b),O in FOLD_O.items(): ENC[f"fold_O_{rg}_b{b}"]=O.cpu().contiguous()
        for (rg,b),(rung,scm,scs) in RUNG.items():
            ENC[f"rung_{rg}_b{b}_sd"]={k:v.cpu() for k,v in rung.state_dict().items()}
            ENC[f"rung_{rg}_b{b}_scaler_mean"]=scm.cpu(); ENC[f"rung_{rg}_b{b}_scaler_std"]=scs.cpu()
        tmp=ENCODER_PT+".tmp"; torch.save(ENC,tmp); os.replace(tmp,ENCODER_PT)
        enc_sha=sha256(ENCODER_PT)
        manifest={"version":"ENCODER_V1 1.0 (2026-07-06)","propose_only":True,"pre_registration":PEN,
            "decoder_source":"decoder_v7 (b1d2f464c00c3ef6)","lexicon":"LEXICON_V3 (71a51619a9bb25c3)",
            "seam_operators":"_l2babel_maps.pt ("+mapsha+")","encode_rules":res["encoder"]["channels"],
            "M1":res["M1"].get("VERDICT"),"M2":res["M2"].get("rollup"),"M3":res["M3"].get("rollup"),
            "encoder_pt_sha256_16":enc_sha,"source_sha256":{"decoder_v7_tensors.pt":d7sha,
                "_v5_floors_recal.json":frecsha,"LEXICON_V3.md":lexsha,"_l2babel_maps.pt":mapsha}}
        tmp=ENCODER_JSON+".tmp"
        with open(tmp,"w",encoding="utf-8") as f: json.dump(manifest,f,indent=1)
        os.replace(tmp,ENCODER_JSON)
        res["encoder"]["encoder_pt_sha256_16"]=enc_sha; res["encoder"]["frozen"]=True
        # well-posedness + offspan tables
        wp_table={"frozen":True,"instrument":"encode-then-decode substitution KL vs recal floors","eps_kl":EPS_KL,
                  "rollup":res["M2"].get("rollup"),"cells":res["M2"]["cells"]}
        with open(WP_JSON+".tmp","w",encoding="utf-8") as f: json.dump(wp_table,f,indent=1)
        os.replace(WP_JSON+".tmp",WP_JSON)
        os_table={"frozen":True,"instrument":"off-span extrapolation, sigma-matched nulls","rollup":res["M3"].get("rollup"),
                  "axes":res["M3"]["axes"]}
        with open(OS_JSON+".tmp","w",encoding="utf-8") as f: json.dump(os_table,f,indent=1)
        os.replace(OS_JSON+".tmp",OS_JSON)
        logln(f"[FREEZE] ENCODER_V1 sha={enc_sha} + WELLPOSEDNESS_TABLE_V1 + OFFSPAN_TABLE_V1")

    # ---- status ----
    if SMOKE:
        c=res["M2"]["cells"]; ok=bool(res["M1"].get("done") and c and all(c[k]["identity_pass"] for k in c))
        # at least one byte-replay must have been checked
        anyreplay=any(c[k]["bank"] is not None for k in c)
        res["status"]="SMOKE-"+("OK" if (ok and anyreplay) else "FAIL")
        res["S0_smoke"]={"M1":res["M1"].get("VERDICT"),"cells":list(c.keys()),"anyreplay":anyreplay}
    else:
        done=(res["M1"].get("done") and len(res["M2"]["cells"])>=39 and res["M2"].get("rollup")
              and res["encoder"].get("frozen"))
        res["status"]=("COMPLETE" if (done and not res["instrument_discrepancy"]) else
                       ("COMPLETE-WITH-DISCREPANCY" if done else "PARTIAL"))
    save_bases(); write_json()
    if M["m"] is not None: del M["m"]; M["m"]=None; free()
except Exception as e:
    res["fatal_error"]={"error":str(e),"trace":traceback.format_exc()}
    logln(f"FATAL {e}\n{traceback.format_exc()}"); res.setdefault("status","FATAL")
write_json()
logln(f"L3 END status={res.get('status')} elapsed={el()}s M2cells={len(res['M2']['cells'])}")
open(os.path.join(DIR,"_l3_smoke_gpu.done" if SMOKE else "_l3_gpu.done"),"w").write(str(res.get("status","?"))+"\n")
logln("*** L3_"+("SMOKE_" if SMOKE else "")+"DONE ***"); LOG.flush(); LOG.close(); print("done")
