# _l6.py -- L6 HUNT THE 5.3% + EXPLAIN THE LAST MISS. PROPOSE-ONLY. GPT-2 124M.
# Pre-registration: FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md ::
#   "L6 -- HUNT THE 5.3% + EXPLAIN THE LAST MISS: ARM A DARK-MASS LOCALIZE/ADJUDICATE/RE-TRANSPLANT
#    (BABEL-OQ-3) + ARM B RUNG CAUSAL STORY ... -- GAP-SCAN + PRE-REGISTRATION (2026-07-06 ~13:4x)".
# Brief: L6_BRIEF_2026-07-06.md (Will 2026-07-06 ~13:25).
# MACHINERY BYTE-VERBATIM: from _l5.py/_l4.py (model loader / capture_h_all / capture_under_delta /
#   proj_compl / wte_y4 / fkl / InjectHook additive residual at BUS[b] / T2 transplant metric klrow+s /
#   rung edit_delta / onset_perpos+M_onset / v_onset positive control / wu_image / logits_under_delta
#   CH-WU contrast) and from _l1.py (FULL V4C snap battery word_battery + gates G1/G3/G4 + rubric)
#   and from _l3.py (M3 off-span proj machinery, L3 class rules -- B3 texture only).
# L6 changes ONLY *which* payload subspaces are transplanted (Arm A) and *which* relations are
# measured (Arm B) -- never the instruments. No weights trained. Zero DB writes.
import json, time, os, math, traceback, gc, subprocess, hashlib, ctypes
import statistics as st
import torch, torch.nn as nn, torch.nn.functional as Fnn

t0=time.time()
DIR=r"C:\Shadow\Dissector\D0_PROGRAM\CONSTRUCTIVE"
SMOKE=os.environ.get("L6_SMOKE")=="1"
LOG=open(os.path.join(DIR,"_l6.log"),"a",encoding="utf-8")
def logln(s):
    s=str(s); LOG.write(f"[L6 {round(time.time()-t0,1):8.1f}s] "+s+"\n"); LOG.flush()
    try: print(s,flush=True)
    except Exception: pass
def el(): return round(time.time()-t0,1)
logln("="*100); logln(f"L6 START smoke={SMOKE} torch={torch.__version__}")
try:
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(),0x4000)
    logln("[ops] priority BelowNormal set")
except Exception as e: logln(f"[ops] priority set failed: {e}")
torch.set_num_threads(6)

# ---------------- locked constants (pre-reg verbatim) ----------------
EPS_KL=0.1871; CERT_BLOCK=512; IND_SEG=64; MB=4; CAP_CHUNK=16; A_EPS=1e-6
VOCAB_SANS_SPECIALS=50256; REGIMES=["prose","code","repetition"]
FRESH_LO,FRESH_HI=24576,32768; REP_SEED=3
N_HOLD=16; TOL_REPLAY=2e-3; TOL_ANCHOR=3e-3; TOL_MAG=1e-2
DEC_V7_SHA="b1d2f464c00c3ef6"; ENC_SHA="6be189567c41e91d"; ENCJ_SHA="365dc3ff592fc6bd"
FREC_SHA="71549ae3afcc8d07"; LEX_SHA="71a51619a9bb25c3"; GRAM_SHA="da6f8a63a061782b"
MAPS_SHA="b43f877af68728df"; WP_SHA="ea5236cbd608a385"; OS_SHA="77dd0948a63bb24f"
# L6-fresh null seed base (pre-reg): +3 A-rank-null, +11 listeners, +17 B2 write-null,
# +23 B3 computed-null, +29 OQ-4 dose-null. Replay stages reuse L5's 20260706 family byte-verbatim.
SEED_A=20260707+3; SEED_B1=20260707+11; SEED_B2=20260707+17; SEED_B3=20260707+23; SEED_OQ4=20260707+29
SEED_L3_J17=20260706+3*101   # _l3.py M3 axis seed for corr_j17_operator (axis index 3), byte-verbatim
N_NULLDIR_A=1 if SMOKE else 3
N_NULL_B=1 if SMOKE else 12
N_NULL_OQ4=1 if SMOKE else 20
B_NULL_BAT=2 if SMOKE else 12
BATTERY_CAP=1 if SMOKE else 8
K_LADDER=[8] if SMOKE else [1,2,4,8,16,32,64,128,256]
CLOSURE_T=0.80
# banked deterministic anchors (byte-replay gates; L5/_l5_result.json + L4/_l4_result.json)
GA1_SBAR=0.9467          # payload-1 readable-gloss transplant sbar (L4 T2 == L5 p1)
GB1_AON=-0.00388         # rung +/-3 behavioral antisym (L5)
GB1_MAG3=7.8544          # rung mag3 (L5)
GB2_A=0.00329            # v_onset validity A at nat_mag (L5)
GB2_MCLEAN=0.9569        # clean M_onset (L5 0.95686, pen anchor 0.9569)
GB3_MII=0.5769           # corr_j17 own-readout Mii(+/-3) (L4 T3)
GB3_M6=1.1467            # corr_j17 own-readout dose (L4 T3, report anchor)
L5_AON6=-0.01023         # rung +/-6 behavioral antisym (L5, OQ-4 target; replay reported)
L4_SIG_J17=2.4676        # corr_j17 sigma at b5 code (L4, report anchor)
FIELD_NAMES={0:"naval/warship",1:"collegiate-sports",2:"special-symbol<->temporal",3:"L0-magnitude/anomalous",
    4:"place-name<->statistics",5:"clause-final/physical-process",6:"epistemic-negative",7:"formula/markup-symbol",
    8:"harm/casualty",9:"sports-team",10:"punctuation-boundary",11:"coastal-storm/geography",12:"local-relation/admin",
    13:"quotation/boundary",14:"comma-boundary",15:"mixed-measurement",16:"spatial-preposition/@",17:"hyphen/@-format",
    18:"@-formatting"}
ROOMS=[2,5,3,4,6]; C_BANKED={0:{"C":-0.6281},16:{"C":-1.5931}}
N_STAND_ANCHOR=64; N_BANK=16
SOFT_WALL_S=5*3600; HARD_WALL_S=6*3600
ATTR_BOUNDS=[2,4,8,10]

RESULT_JSON=os.path.join(DIR,"_l6_result_SMOKE.json" if SMOKE else "_l6_result.json")
BASES_PT=os.path.join(DIR,"_l6_bases_SMOKE.pt" if SMOKE else "_l6_bases.pt")
torch.manual_seed(1234)

PEN=("FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md :: 'L6 -- HUNT THE 5.3% + EXPLAIN THE LAST MISS: ARM A "
     "DARK-MASS LOCALIZE/ADJUDICATE/RE-TRANSPLANT (BABEL-OQ-3) + ARM B RUNG CAUSAL STORY (LISTENERS / "
     "WRITER-VS-READER incl. BABEL-OQ-4 / corr_j17 LEAKAGE-vs-GENUINE) -- GAP-SCAN + PRE-REGISTRATION "
     "(2026-07-06 ~13:4x)'")
res={"experiment":"L6 hunt the 5.3% + explain the last miss: Arm A dark-mass localize (SVD rank-ladder + "
     "greedy) / adjudicate (L1 battery) / re-transplant gate (BABEL-OQ-3); Arm B rung causal story: "
     "listeners fan-out, writer-vs-reader incl. BABEL-OQ-4 honest-N dose null, corr_j17 leakage-vs-genuine "
     "echo decomposition. Consumes FROZEN ENCODER_V1; machinery byte-verbatim L5/L4/L1/L3. GPT-2 124M.",
     "date":"2026-07-06","propose_only":True,"pre_registration":PEN,
     "locked":{"tol_replay":TOL_REPLAY,"n_nulldir_A":N_NULLDIR_A,"n_null_B":N_NULL_B,"n_null_OQ4":N_NULL_OQ4,
        "k_ladder":K_LADDER,"closure_T":CLOSURE_T,"battery_cap":BATTERY_CAP,"b_null_battery":B_NULL_BAT,
        "A1_bands":"LOCALIZED-LOW-RANK k_loc<=8 / LOCALIZED-MID 8<k_loc<=32 / DIFFUSE k_loc>32 ; "
                   "bet DIFFUSE40/MID35/LOWRANK25",
        "A2_bands":"f=(NAMED+NAMED-REGIME-SPECIFIC)/n_adjudicated: ALL-DARK f=0 / NAMED-SOME 0<f<0.5 / "
                   "NAMED-MAJORITY f>=0.5 ; bet ALLDARK45/SOME35/MAJORITY20",
        "A3_gate":"residKL(p_sel)<=0.1871 else LOCALIZATION-INCOMPLETE",
        "B1_bands":"SILENT 0 / CONCENTRATED 1-3 / BROADCAST >=4 ; bet CONCENTRATED40/SILENT35/BROADCAST25",
        "B2_bands":"COWRITER if |A_on6|>null95_20 & sign==A_on / READER if reader_valid & control_writes / "
                   "else INDEPENDENT ; bet READER45/INDEPENDENT30/COWRITER25",
        "B3_bands":"LEAKAGE |Mcomp|<=null95c / MIXED >null95c & <|Mdirect| / GENUINE >null95c & >=|Mdirect| "
                   "& signs ; bet MIXED40/LEAKAGE35/GENUINE25"},
     "config":{"n_hold":N_HOLD,"mb":MB,"cap_chunk":CAP_CHUNK,"cert_block":CERT_BLOCK,"ind_seg":IND_SEG,
        "precision":"fp32","tf32":"off","attn":"eager","seed":1234,"smoke":SMOKE},
     "gpu_free_checks":[],"instrument_discrepancy":[],"gates":{},
     "armA":{},"armB":{},"verdicts":{},"status":"INIT"}

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
        for k in ("armA","armB","gates","verdicts","gpu_free_checks","instrument_discrepancy"):
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
def flag(stage,name,why):
    res["instrument_discrepancy"].append({"stage":stage,"name":name,"why":str(why)}); write_json()
    logln(f"[FB-B {stage}] {name}: {why}")

# ---------------- model (v7/l4/l5 loader verbatim) ----------------
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

# ---------------- KL kernel + inject (v7/l4/l5 verbatim) ----------------
def fkl(yt,yp):
    logp=Fnn.log_softmax(yt,-1); p=logp.exp(); lp=Fnn.log_softmax(yp,-1)
    return (p*(logp-lp)).sum(-1)
def klrow(pt,pp):
    logpt=Fnn.log_softmax(pt,-1); p=logpt.exp(); logpp=Fnn.log_softmax(pp,-1)
    return (p*(logpt-logpp)).sum(-1)
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

# logits under a delta + CH-WU contrast (L4 verbatim)
def logits_under_delta(ids_cpu,injhook,delta_full_g,readouts,pos_lo,pos_hi,Yclean=None,want_meanlogit=False):
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
                d_=(lgp-Yclean[ci][:,pos_lo:pos_hi,:].float()); mlt+=d_.reshape(-1,d_.shape[-1]).sum(0); mcnt+=d_.shape[0]*d_.shape[1]
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

# L1-style capture (selected boundaries only; battery banks)
def capture_which(ids_cpu,chunk,tag,which):
    model=M["m"]; nL=M["nL"]; N=ids_cpu.shape[0]
    buf={}; handles=[]
    def mk(key):
        def h(mod,inp,out): buf[key]=(out[0] if isinstance(out,tuple) else out).detach()
        return h
    handles.append(M["drop"].register_forward_hook(mk(0)))
    for L in range(nL): handles.append(M["blocks"][L].register_forward_hook(mk(L+1)))
    acc={b:[] for b in which}
    with torch.no_grad():
        for c0 in range(0,N,chunk):
            c1=min(N,c0+chunk); _=model(ids_cpu[c0:c1].to('cuda'),use_cache=False)
            for b in which: acc[b].append(buf[b].reshape(-1,M["d"]).cpu())
    for hd in handles: hd.remove()
    H={b:torch.cat(acc[b],0) for b in which}
    logln(f"[capture {tag}] boundaries={sorted(which)} shape={tuple(H[which[0]].shape)} chunk={chunk}")
    return H

class LinearRung(nn.Module):
    def __init__(self,fin,d): super().__init__(); self.w=nn.Linear(fin,d)
    def forward(self,x): return self.w(x)

# ---------------- SnapHook + snap battery (V4/_l1.py verbatim) ----------------
class SnapHook:
    def __init__(self,mod,is_tuple):
        self.is_tuple=is_tuple; self.st={"on":False,"P":None,"ci":None,"fac":None}
        self.handle=mod.register_forward_hook(self._hook)
    def _hook(self,mod,inp,out):
        if not self.st["on"]: return None
        w=out[0] if self.is_tuple else out; wP=w@self.st["P"]; coef=wP@self.st["ci"]
        add=((self.st["fac"]-1.0)*coef).unsqueeze(-1)*self.st["ci"]; w2=wP+add
        return (w2,)+tuple(out[1:]) if self.is_tuple else w2
    def close(self): self.handle.remove()
def measure_class_snap_cap(model,snaphooks,ids,P,ci,fac,class_idx,mb,cap_blocks):
    S=ids.shape[0]; outs=[]; capbuf={cb:[] for cb in cap_blocks}; tmp={}
    handles=[]
    def mk(key):
        def h(mod,inp,out): tmp[key]=(out[0] if isinstance(out,tuple) else out).detach()
        return h
    for cb in cap_blocks: handles.append(M["blocks"][cb].register_forward_hook(mk(cb)))
    with torch.no_grad():
        for s0 in range(0,S,mb):
            s1=min(S,s0+mb)
            for h in snaphooks: h.st["on"]=True; h.st["P"]=P; h.st["ci"]=ci; h.st["fac"]=fac[s0:s1]
            lg=model(ids[s0:s1],use_cache=False).logits
            for h in snaphooks: h.st["on"]=False
            cols=[lg[:,:,cid].float().mean(-1) for cid in class_idx]
            outs.append(torch.stack(cols,-1).cpu())
            for cb in cap_blocks: capbuf[cb].append(tmp[cb].cpu())
            del lg
    for hd in handles: hd.remove()
    caps={cb:torch.cat(capbuf[cb],0) for cb in cap_blocks}
    return torch.cat(outs,0),caps
def snap_identity_check(ids4):
    model=M["m"]; d=M["d"]; nL=M["nL"]
    ref=[]
    with torch.no_grad():
        for s0 in range(0,ids4.shape[0],MB):
            ref.append(model(ids4[s0:s0+MB],use_cache=False).logits.detach())
    snap=[SnapHook(M["blocks"][L].attn,True) for L in range(nL)]
    P=torch.eye(d,device='cuda'); ci=torch.zeros(d,device='cuda'); ci[0]=1.0
    ones=torch.ones(ids4.shape[0],CERT_BLOCK,device='cuda')
    dmax=0.0
    with torch.no_grad():
        ii=0
        for s0 in range(0,ids4.shape[0],MB):
            for h in snap: h.st["on"]=True; h.st["P"]=P; h.st["ci"]=ci; h.st["fac"]=ones[s0:s0+MB]
            lg=model(ids4[s0:s0+MB],use_cache=False).logits
            for h in snap: h.st["on"]=False
            dmax=max(dmax,float((lg-ref[ii]).abs().max())); ii+=1; del lg
    for h in snap: h.close()
    return dmax
def pearson(a,b):
    a=a.reshape(-1).double(); b=b.reshape(-1).double()
    a=a-a.mean(); b=b-b.mean()
    den=(a.norm()*b.norm()).clamp(min=1e-12)
    return float((a@b)/den)

# ======================================================================================
# MAIN
# ======================================================================================
try:
    ensure_model()
    d=M["d"]; nL=M["nL"]; tok=M["tok"]; wte_g=M["wte"]; lnf_g=M["lnf"].to('cuda'); lnf_cpu=M["lnf"].cpu()
    lnf_gpu=lnf_g; wte_cpu=wte_g.cpu()

    # ---- GATE-0: hashes (ALL 8 locked; FB-A on any breach) ----
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

    # ---- load decoder_v7 + ENCODER_V1 (verbatim l4/l5) ----
    D7=torch.load(os.path.join(DIR,"decoder_v7_tensors.pt"),map_location="cpu",weights_only=False)
    C=D7["C"].float(); B2=D7["B2"].float(); Q35=D7["Q35"].float(); Qu=D7["Q_union"].float()
    Qa=D7["Q_attn"].float(); Qm=D7["Q_mlp"].float()
    mu=D7["mu"].float(); wteW=D7["wte_W"].float(); wtec=D7["wte_c"].float()
    read_W=D7["read_W"].float(); Vk=D7["m0_repera_Vk_recal"].float()
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
    C_g=C.to('cuda'); B2_g=B2.to('cuda'); Q35_g=Q35.to('cuda'); span5=torch.cat([B2_g,Q35_g],1)
    Qu_g=Qu.to('cuda'); Vk_g=Vk.to('cuda'); mu_g={b:mu[b].to('cuda') for b in range(nL+1)}
    wteW_g=wteW.to('cuda'); wtec_g=wtec.to('cuda')
    read_W_g={b:read_W[b].to('cuda') for b in range(read_W.shape[0])}
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
    MAPS=torch.load(os.path.join(DIR,"_l2babel_maps.pt"),map_location="cpu",weights_only=False)
    W_rep={b:MAPS[f"W_repetition_b{b}"].float() for b in (6,7,8)}

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

    # ================= GATE-0 identity-inject exact-zero per regime (matched batch shape MB) =========
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
    # ARM A -- A1 LOCALIZE the dark transplant carrier (prose b6, 16 pairs, T2 metric verbatim)
    # =========================================================================================
    armA_flagged=False
    if not res["armA"].get("a1_done"):
        gpu_free_check("armA-A1")
        bA=6; regime="prose"
        idsA,capA,YclA=get_regime(regime); N_A=idsA.shape[0]
        XcA=capA[bA].to('cuda')-mu_g[bA]; ids_flat_g=idsA.reshape(-1).to('cuda')
        b2P=(XcA@B2_g)@B2_g.t(); q35P=(XcA@Q35_g)@Q35_g.t(); y4A=wte_y4(ids_flat_g,bA)
        recon1=(mu_g[bA]+b2P+q35P+y4A)                     # readable gloss (L4 T2 payload; sbar_1 anchor)
        recon3=(mu_g[bA]+XcA)                              # full raw ceiling
        dark=proj_compl(XcA)                               # [ntok,768] dark_i := proj_compl(x_i - mu_b6)
        dark_span_leak=float((dark@span5).abs().max())
        PAIRS_A=([(0,1)] if SMOKE else [(i,(i+1)%N_A) for i in range(N_A)])
        injA=InjectHook(M["blocks"][bA-1])
        # clean per-block logits + klBA cache (deterministic [1,512] forwards; identical to L5 usage)
        LGC={}; KLBA={}
        with torch.no_grad():
            for i_ in range(N_A):
                LGC[i_]=M["m"](idsA[i_:i_+1].to('cuda'),use_cache=False).logits[0].float()
        for (ai,bi) in PAIRS_A: KLBA[(ai,bi)]=klrow(LGC[bi],LGC[ai]).clamp(min=1e-9)
        def sweep_payload(recon_flat,keep_pairs=False):
            recon=recon_flat.reshape(N_A,CERT_BLOCK,d)
            per=[]
            for (ai,bi) in PAIRS_A:
                dstate=(recon[ai]-recon[bi])
                with torch.no_grad():
                    injA.add=dstate.unsqueeze(0); injA.on=True
                    lgInj=M["m"](idsA[bi:bi+1].to('cuda'),use_cache=False).logits[0].float()
                    injA.on=False; injA.add=None
                klBA=KLBA[(ai,bi)]; klInjA=klrow(lgInj,LGC[ai])
                s=float(((klBA-klInjA)/klBA).mean()); rk=float(klInjA.mean())
                per.append({"A":ai,"B":bi,"s":round(s,4),"residKL":round(rk,5)}); del lgInj
            sbar=sum(p["s"] for p in per)/len(per)
            residKL=sum(p["residKL"] for p in per)/len(per)
            se=(st.pstdev([p["s"] for p in per])/math.sqrt(len(per))) if len(per)>1 else 0.0
            return sbar,residKL,se,(per if keep_pairs else None)
        # ---- GA-1: payload-1 byte-replay ----
        if "ga1" not in res["armA"]:
            sb1,rk1,se1,pp1=sweep_payload(recon1,keep_pairs=True)
            dev=abs(sb1-GA1_SBAR); ga1_ok=bool(dev<=TOL_REPLAY)
            res["armA"]["ga1"]={"sbar1":round(sb1,4),"residKL1":round(rk1,5),"se":round(se1,4),
                                "banked":GA1_SBAR,"dev":round(dev,5),"pass":ga1_ok,"per_pair":pp1}
            if not ga1_ok and not SMOKE: flag("armA","GA-1_payload1_replay",f"sbar1={sb1} banked={GA1_SBAR} dev={dev}")
            write_json(); logln(f"[GA-1] sbar1={sb1:.4f} banked={GA1_SBAR} dev={dev:.5f} -> {'PASS' if ga1_ok else 'FAIL'}")
        sbar1=res["armA"]["ga1"]["sbar1"]
        armA_flagged=not res["armA"]["ga1"]["pass"]
        if "p3" not in res["armA"]:
            sb3,rk3,se3,pp3=sweep_payload(recon3,keep_pairs=True)
            res["armA"]["p3"]={"sbar3":round(sb3,4),"residKL3":round(rk3,5),"per_pair":pp3}
            write_json(); logln(f"[armA p3] sbar3={sb3:.4f} residKL={rk3:.5f}")
        sbar3=res["armA"]["p3"]["sbar3"]
        denomA=sbar3-sbar1
        def closure_of(sb): return (sb-sbar1)/denomA if abs(denomA)>1e-6 else None
        # ---- SVD of dark pair-deltas ----
        if "armA_Vh256" not in BASES:
            dd=dark.reshape(N_A,CERT_BLOCK,d)
            ddark=torch.cat([ (dd[ai]-dd[bi]) for (ai,bi) in PAIRS_A ],0)   # [n_pairs*512, 768]
            U_,S_,Vh_=torch.linalg.svd(ddark,full_matrices=False)
            BASES["armA_Vh256"]=Vh_[:256].cpu(); BASES["armA_svals"]=S_.cpu()
            save_bases()
            sv=S_.cpu().tolist()
            res["armA"]["svd"]={"n_rows":int(ddark.shape[0]),"svals_top16":[round(x,2) for x in sv[:16]],
                "sval_1":round(sv[0],2),"sval_8":round(sv[7],2) if len(sv)>7 else None,
                "sval_32":round(sv[31],2) if len(sv)>31 else None,
                "sval_256":round(sv[255],2) if len(sv)>255 else None,
                "dark_span5_leak_max":dark_span_leak}
            write_json(); logln(f"[armA SVD] rows={ddark.shape[0]} sv1={sv[0]:.1f} sv8={sv[7]:.1f} sv32={sv[31]:.1f}")
            del ddark,U_,S_,Vh_
        Vh256=BASES["armA_Vh256"].to('cuda')                                  # [256,768]
        # ---- RANK LADDER ----
        res["armA"].setdefault("ladder",{})
        for k in K_LADDER:
            kk=str(k)
            if kk in res["armA"]["ladder"]: continue
            Vk_=Vh256[:k].t()                                                 # [768,k]
            pk=recon1+(dark@Vk_)@Vk_.t()
            sb,rk,se_,_=sweep_payload(pk)
            cl=closure_of(sb)
            res["armA"]["ladder"][kk]={"sbar":round(sb,4),"residKL":round(rk,5),
                "closure":(round(cl,4) if cl is not None else None)}
            write_json(); logln(f"[armA ladder k={k}] sbar={sb:.4f} residKL={rk:.5f} closure={cl}")
        # ---- GREEDY over top-16 SVD dirs (max marginal closure per step, up to 8) ----
        if "greedy" not in res["armA"]:
            if SMOKE:
                res["armA"]["greedy"]={"steps":[],"skipped":"smoke"}
            else:
                sel=[]; steps=[]; best_cl=-9.9
                cand_all=list(range(16))
                while len(sel)<8:
                    best=None
                    for c in cand_all:
                        if c in sel: continue
                        Vs=Vh256[sel+[c]].t()
                        pk=recon1+(dark@Vs)@Vs.t()
                        sb,rk,_,_=sweep_payload(pk)
                        cl=closure_of(sb)
                        if best is None or (cl is not None and cl>best[1]): best=(c,cl,sb,rk)
                    sel.append(best[0]); best_cl=best[1]
                    steps.append({"j":len(sel),"dir":int(best[0]),"closure":round(best[1],4),
                                  "sbar":round(best[2],4),"residKL":round(best[3],5)})
                    logln(f"[armA greedy j={len(sel)}] +dir{best[0]} closure={best[1]:.4f}")
                    if best_cl>=CLOSURE_T: break
                res["armA"]["greedy"]={"steps":steps,"selected_order":sel}
            write_json()
        # ---- k_loc + verdict band ----
        if "a1_verdict" not in res["armA"]:
            lad=res["armA"]["ladder"]
            ladder_k=None
            for k in sorted([int(x) for x in lad],key=int):
                c=lad[str(k)]["closure"]
                if c is not None and c>=CLOSURE_T: ladder_k=k; break
            greedy_j=None; gsteps=res["armA"]["greedy"].get("steps",[])
            for s_ in gsteps:
                if s_["closure"]>=CLOSURE_T: greedy_j=s_["j"]; break
            cands=[x for x in (ladder_k,greedy_j) if x is not None]
            k_loc=min(cands) if cands else None
            if k_loc is None: band="DIFFUSE"
            elif k_loc<=8: band="LOCALIZED-LOW-RANK"
            elif k_loc<=32: band="LOCALIZED-MID"
            else: band="DIFFUSE"
            # SELECTED SET: greedy prefix if it won, else top-k_loc SVD dirs
            if greedy_j is not None and (ladder_k is None or greedy_j<=ladder_k):
                sel_idx=res["armA"]["greedy"]["selected_order"][:greedy_j]; sel_src="greedy"
            elif ladder_k is not None:
                sel_idx=list(range(ladder_k)); sel_src="ladder"
            else:
                # DIFFUSE: A2 adjudicates top-8 SVD anyway; A3 verdict payload = best ladder k (stated)
                bestk=max(lad,key=lambda kk:(lad[kk]["closure"] if lad[kk]["closure"] is not None else -9))
                sel_idx=list(range(min(8,Vh256.shape[0]))); sel_src=f"diffuse-top8-svd (A3 payload=ladder k={bestk})"
            res["armA"]["a1_verdict"]={"ladder_k":ladder_k,"greedy_j":greedy_j,"k_loc":k_loc,
                "H_L6_A1":band,"selected_source":sel_src,"selected_idx":sel_idx,
                "bet":"DIFFUSE40/MID35/LOWRANK25","bet_favorite_hit":bool(band=="DIFFUSE")}
            write_json(); logln(f"[A1 VERDICT] ladder_k={ladder_k} greedy_j={greedy_j} k_loc={k_loc} -> {band}")
        a1v=res["armA"]["a1_verdict"]
        sel_idx=a1v["selected_idx"]
        Vsel=Vh256[sel_idx].t()                                                # [768,|sel|]
        BASES["armA_selected_dirs"]=Vsel.cpu(); save_bases()
        # A3 verdict payload: selected set; if DIFFUSE, best ladder k (stated)
        if a1v["H_L6_A1"]=="DIFFUSE" and not SMOKE:
            lad=res["armA"]["ladder"]
            bestk=int(max(lad,key=lambda kk:(lad[kk]["closure"] if lad[kk]["closure"] is not None else -9)))
            Vver=Vh256[:bestk].t(); ver_rank=bestk; ver_src=f"best-ladder-k{bestk}"
        else:
            Vver=Vsel; ver_rank=len(sel_idx); ver_src=a1v["selected_source"]
        sel_dark=(dark@Vver)@Vver.t()
        # ---- SPECIFICITY null (random rank-matched ON-subspace of the dark complement, norm-matched) ----
        if "specificity" not in res["armA"]:
            gpA=torch.Generator(device='cuda').manual_seed(SEED_A)
            nsel=sel_dark.norm(dim=1,keepdim=True)
            cls_=[]; rks_=[]
            for _ in range(N_NULLDIR_A):
                Rr=torch.randn(d,ver_rank,generator=gpA,device='cuda')
                Rc=proj_compl(Rr.t()).t()                                      # columns into dark complement
                Qr,_=torch.linalg.qr(Rc)                                       # [768,rank] ON
                nd=(dark@Qr)@Qr.t()
                nn_=nd.norm(dim=1,keepdim=True).clamp(min=1e-9)
                nd=nd*(nsel/nn_)
                sb,rk,_,_=sweep_payload(recon1+nd)
                cls_.append(closure_of(sb)); rks_.append(rk)
            res["armA"]["specificity"]={"rank":ver_rank,"n_draws":N_NULLDIR_A,
                "closure_null_draws":[round(x,4) for x in cls_],
                "closure_null_mean":round(sum(cls_)/len(cls_),4),
                "residKL_null_mean":round(sum(rks_)/len(rks_),5),"seed":SEED_A}
            write_json(); logln(f"[armA specificity] closure_null={res['armA']['specificity']['closure_null_mean']}")
        # ---- A3 RE-TRANSPLANT GATE ----
        if "a3" not in res["armA"]:
            sb_s,rk_s,se_s,pp_s=sweep_payload(recon1+sel_dark,keep_pairs=True)
            cl_s=closure_of(sb_s)
            gate_pass=bool(rk_s<=EPS_KL)
            res["armA"]["a3"]={"payload":ver_src,"rank":ver_rank,"sbar_sel":round(sb_s,4),
                "closure_sel":(round(cl_s,4) if cl_s is not None else None),"residKL_sel":round(rk_s,5),
                "recal_floor":EPS_KL,"GATE_PASS":gate_pass,
                "verdict_text":("RE-TRANSPLANT GATE PASS: certified+recovered payload within recal floor of raw"
                                if gate_pass else "LOCALIZATION-INCOMPLETE"),
                "closure_null_mean":res["armA"]["specificity"]["closure_null_mean"],
                "residKL_null_mean":res["armA"]["specificity"]["residKL_null_mean"],"per_pair":pp_s}
            write_json(); logln(f"[A3] sbar_sel={sb_s:.4f} closure={cl_s} residKL={rk_s:.5f} vs floor {EPS_KL} "
                                f"-> {'PASS' if gate_pass else 'LOCALIZATION-INCOMPLETE'}")
        # ---- PER-BOUNDARY ATTRIBUTION (report-only texture; FB-C droppable) ----
        if "attribution" not in res["armA"] and not SMOKE and el()<SOFT_WALL_S:
            attr={}
            for bb_ in ATTR_BOUNDS:
                Xb=capA[bb_].to('cuda')-mu_g[bb_]
                b2b=(Xb@B2_g)@B2_g.t(); q35b=(Xb@Q35_g)@Q35_g.t(); y4b=wte_y4(ids_flat_g,bb_)
                r1b=(mu_g[bb_]+b2b+q35b+y4b); r3b=(mu_g[bb_]+Xb)
                injB_=InjectHook(M["blocks"][bb_-1])
                def sweep_b(recon_flat,injx):
                    recon=recon_flat.reshape(N_A,CERT_BLOCK,d); ss=[]
                    for (ai,bi) in PAIRS_A:
                        dstate=(recon[ai]-recon[bi])
                        with torch.no_grad():
                            injx.add=dstate.unsqueeze(0); injx.on=True
                            lgInj=M["m"](idsA[bi:bi+1].to('cuda'),use_cache=False).logits[0].float()
                            injx.on=False; injx.add=None
                        klBA=KLBA[(ai,bi)]; ss.append(float(((klBA-klrow(lgInj,LGC[ai]))/klBA).mean()))
                    return sum(ss)/len(ss)
                s1b=sweep_b(r1b,injB_); s3b=sweep_b(r3b,injB_)
                injB_.close()
                dkb=proj_compl(Xb)
                dfrac=float((dkb*dkb).sum(1).mean()/ (Xb*Xb).sum(1).mean())
                attr[f"b{bb_}"]={"sbar1":round(s1b,4),"sbar3":round(s3b,4),
                    "dark_gap":round(s3b-s1b,4),"dark_mass_frac":round(dfrac,4)}
                logln(f"[armA attr b{bb_}] sbar1={s1b:.4f} sbar3={s3b:.4f} gap={s3b-s1b:.4f} dark={dfrac:.4f}")
                del Xb,b2b,q35b,y4b,r1b,r3b,dkb; free()
            attr["b6_banked"]={"sbar1":sbar1,"sbar3":sbar3,"dark_gap":round(sbar3-sbar1,4),
                "dark_mass_frac":0.0483}
            res["armA"]["attribution"]=attr; write_json()
        injA.close()
        res["armA"]["a1_done"]=True; write_json()
        del XcA,b2P,q35P,y4A,recon1,recon3,dark,sel_dark,LGC,KLBA; free()

    # =========================================================================================
    # ARM B -- setup + GB-1 (rep regime, rung machinery byte-verbatim L5)
    # =========================================================================================
    gpu_free_check("armB")
    bb=6; rg="repetition"
    idsR,capR,YclR=get_regime(rg); N_R=idsR.shape[0]
    injR=InjectHook(M["blocks"][bb-1])
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
    rung_img_dir=oh_real.mean(0); rung_img_dir=rung_img_dir/rung_img_dir.norm().clamp(min=1e-6)
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
    # ---- GB-1: rung +/-3 behavioral replay + mag3 ----
    if "gb1" not in res["armB"]:
        dv3,mag3_=rung_edit_delta(3); dvm3,_=rung_edit_delta(-3)
        Mp3=onset_mean(injR,dv3); Mm3=onset_mean(injR,dvm3)
        A_on=(Mp3-Mm3)/2.0
        devA=abs(A_on-GB1_AON); devM=abs(mag3_-GB1_MAG3)
        gb1_ok=bool(devA<=TOL_REPLAY and devM<=TOL_MAG)
        res["armB"]["gb1"]={"A_on":round(A_on,5),"banked_A":GB1_AON,"dev_A":round(devA,6),
            "mag3":round(mag3_,4),"banked_mag3":GB1_MAG3,"dev_mag":round(devM,5),
            "M_plus3":round(Mp3,5),"M_minus3":round(Mm3,5),"pass":gb1_ok}
        if not gb1_ok and not SMOKE: flag("armB","GB-1_rung_replay",res["armB"]["gb1"])
        write_json(); logln(f"[GB-1] A_on={A_on:.5f} (banked {GB1_AON}) mag3={mag3_:.4f} -> {'PASS' if gb1_ok else 'FAIL'}")
    gb1=res["armB"]["gb1"]; mag3=gb1["mag3"]; A_on=gb1["A_on"]
    b1_flagged=not gb1["pass"]

    # =========================================================================================
    # B1 -- LISTENERS (who consumes the rung's output)
    # =========================================================================================
    if not res["armB"].get("b1_done"):
        gpu_free_check("armB-B1")
        WANT=[7,8] if SMOKE else [7,8,9,10,11,12]
        posm=torch.arange(IND_SEG,CERT_BLOCK)
        dvp,_=rung_edit_delta(3); dvm,_=rung_edit_delta(-3)
        v3=dvp[0,IND_SEG,:].clone()                                            # rung writable image (constant)
        antisym_dev=float((dvp+dvm).abs().max())
        const_dev=float((dvp[:,IND_SEG:,:]-v3).abs().max())
        capP=capture_under_delta(idsR,injR,dvp,WANT); capM=capture_under_delta(idsR,injR,dvm,WANT)
        # per-boundary clean stds (certified readers)
        sd_core={}; sd_door={}; Dmet={}; Dcomp={}
        for b_ in WANT:
            Xb=(capR[b_].to('cuda')-mu_g[b_]).reshape(N_R,CERT_BLOCK,d)[:,posm,:].reshape(-1,d)
            sd_core[b_]=(Xb@C_g).std(0).clamp(min=1e-9)
            sd_door[b_]=((Xb@Qu_g)@read_W_g[b_].t()).std(0).clamp(min=1e-9)
            D_=((capP[b_]-capM[b_])/2.0).to('cuda').reshape(N_R,CERT_BLOCK,d)[:,posm,:]
            Dmet[b_]=D_; Dcomp[b_]=D_-v3                                       # direct-carry decomposition
            del Xb
        def chan_stats(Dg,b_):
            # returns (z_core[19],se_core[19],z_door[19],se_door[19]) in z units
            flat=Dg.reshape(-1,d)
            gc_=(flat@C_g)/sd_core[b_]; gd_=((flat@Qu_g)@read_W_g[b_].t())/sd_door[b_]
            out=[]
            for gz in (gc_,gd_):
                blk=gz.reshape(N_R,-1,19).mean(1)                              # [16,19] per-block means
                mz=blk.mean(0); se=blk.std(0,unbiased=True)/math.sqrt(N_R)
                out.append((mz,se))
            return out[0][0],out[0][1],out[1][0],out[1][1]
        stats={}
        for b_ in WANT:
            zc,sec,zd,sed=chan_stats(Dcomp[b_],b_)
            stats[b_]={"core_z":zc.cpu(),"core_se":sec.cpu(),"door_z":zd.cpu(),"door_se":sed.cpu()}
        # NULL: N_NULL_B random unit DARK-complement dirs at mag3, same decomposition, max|z| over all cells
        gpB1=torch.Generator(device='cuda').manual_seed(SEED_B1)
        null_max=[]
        for it in range(N_NULL_B):
            r=torch.randn(d,generator=gpB1,device='cuda'); r=proj_compl(r.unsqueeze(0)).squeeze(0)
            r=r/r.norm().clamp(min=1e-6)
            dp=(mag3*r).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous(); dp=dp.clone(); dp[:, :IND_SEG, :]=0.0
            dm=(-mag3*r).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous(); dm=dm.clone(); dm[:, :IND_SEG, :]=0.0
            cP=capture_under_delta(idsR,injR,dp,WANT); cM=capture_under_delta(idsR,injR,dm,WANT)
            mx=0.0
            for b_ in WANT:
                D_=((cP[b_]-cM[b_])/2.0).to('cuda').reshape(N_R,CERT_BLOCK,d)[:,posm,:]-(mag3*r)
                zc,_,zd,_=chan_stats(D_,b_)
                mx=max(mx,float(zc.abs().max()),float(zd.abs().max()))
                del D_
            null_max.append(mx); del cP,cM
            logln(f"[B1 null {it+1}/{N_NULL_B}] max|z|={mx:.4f}")
        null95_max=pct95(null_max)
        # listeners: distinct (read-type x field) with |z|>null95_max AND |z|>=2SE at the clearing boundary
        listeners=[]
        for rt in ("core","door"):
            for f_ in range(19):
                hits=[]
                for b_ in WANT:
                    z=float(stats[b_][f"{rt}_z"][f_]); se=float(stats[b_][f"{rt}_se"][f_])
                    if abs(z)>null95_max and abs(z)>=2*se: hits.append({"b":b_,"z":round(z,4),"se":round(se,5)})
                if hits:
                    zb=max(hits,key=lambda h:abs(h["z"]))
                    listeners.append({"read":rt,"field":f_,"name":FIELD_NAMES.get(f_,f"f{f_}"),
                                      "best":zb,"n_bounds_clear":len(hits)})
        N_listen=len(listeners)
        # POSITIVE-CONTROL GATE (licenses SILENT only): naval C[:,0] at mag3, NO carry subtraction, b7
        vnav=C_g[:,0]
        dpn=(mag3*vnav).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous(); dpn=dpn.clone(); dpn[:, :IND_SEG, :]=0.0
        dmn=(-mag3*vnav).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous(); dmn=dmn.clone(); dmn[:, :IND_SEG, :]=0.0
        cPn=capture_under_delta(idsR,injR,dpn,[7]); cMn=capture_under_delta(idsR,injR,dmn,[7])
        Dn=((cPn[7]-cMn[7])/2.0).to('cuda').reshape(N_R,CERT_BLOCK,d)[:,posm,:]
        z_nav=float(((Dn.reshape(-1,d)@C_g)/sd_core[7])[:,0].mean())
        pc_pass=bool(abs(z_nav)>null95_max)
        if SMOKE and 7 not in WANT: pc_pass=True
        # band (mechanical)
        if N_listen==0: band=("SILENT" if pc_pass else "NO-VERDICT-SILENT-UNLICENSED")
        elif N_listen<=3: band="CONCENTRATED"
        else: band="BROADCAST"
        # SEAM TEXTURE (report-only): predicted D_g(b+1)=W_rep_b @ D_g(b), seams 6->7->8->9, FULL delta
        seam={}
        if not SMOKE and el()<SOFT_WALL_S:
            Dg={6:(v3@C_g).cpu()}
            for b_ in (7,8,9):
                if b_ in Dmet: Dg[b_]=Dmet[b_].reshape(-1,d).mean(0).cpu()@C
            for b_ in (6,7,8):
                if b_ in Dg and (b_+1) in Dg:
                    pred=W_rep[b_]@Dg[b_]
                    cosv=float((pred@Dg[b_+1])/max(1e-12,float(pred.norm())*float(Dg[b_+1].norm())))
                    seam[f"{b_}->{b_+1}"]={"cos":round(cosv,4),
                        "mag_ratio":round(float(Dg[b_+1].norm())/max(1e-12,float(pred.norm())),4)}
        # ABLATION TEXTURE (report-only): delta=-oh_real, one capture, top-5 moved channels (carry-subtracted)
        abl_top=[]
        if not SMOKE and el()<SOFT_WALL_S:
            dab=(-oh_real).reshape(N_R,CERT_BLOCK,d).contiguous(); dab=dab.clone(); dab[:, :IND_SEG, :]=0.0
            zero_dummy=torch.zeros(1)
            cap0m=capture_under_delta(idsR,None,zero_dummy,WANT)
            capAb=capture_under_delta(idsR,injR,dab,WANT)
            ohm=oh_real.reshape(N_R,CERT_BLOCK,d)[:,posm,:]
            cells=[]
            for b_ in WANT:
                Da=(capAb[b_]-cap0m[b_]).to('cuda').reshape(N_R,CERT_BLOCK,d)[:,posm,:]+ohm
                zc,_,zd,_=chan_stats(Da,b_)
                for f_ in range(19):
                    cells.append(("core",f_,b_,float(zc[f_]))); cells.append(("door",f_,b_,float(zd[f_])))
                del Da
            cells.sort(key=lambda x:-abs(x[3]))
            abl_top=[{"read":c[0],"field":c[1],"name":FIELD_NAMES.get(c[1],""),"b":c[2],"z":round(c[3],4)}
                     for c in cells[:5]]
            del cap0m,capAb,ohm
        top_cells=[]
        for b_ in WANT:
            for rt in ("core","door"):
                zz=stats[b_][f"{rt}_z"]
                for f_ in range(19): top_cells.append((rt,f_,b_,float(zz[f_])))
        top_cells.sort(key=lambda x:-abs(x[3]))
        res["armB"]["b1"]={"bounds":WANT,"n_null":N_NULL_B,"null95_max":round(null95_max,4),
            "null_max_draws":[round(x,4) for x in null_max],
            "antisym_dev":antisym_dev,"const_dev":const_dev,
            "listeners":listeners,"N_listen":N_listen,
            "top8_cells_z":[{"read":c[0],"field":c[1],"b":c[2],"z":round(c[3],4)} for c in top_cells[:8]],
            "positive_control":{"z_naval_b7_no_carry_sub":round(z_nav,4),"clears":pc_pass},
            "seam_texture":seam,"ablation_top5":abl_top,
            "H_L6_B1":band,"bet":"CONCENTRATED40/SILENT35/BROADCAST25",
            "bet_favorite_hit":bool(band=="CONCENTRATED"),
            "instrument_flagged":b1_flagged}
        res["armB"]["b1_done"]=True; write_json()
        logln(f"[B1 VERDICT] N_listen={N_listen} null95_max={null95_max:.4f} pc={pc_pass} -> {band}")
        del capP,capM,Dmet,Dcomp,stats; free()

    # =========================================================================================
    # B2 -- WRITER VS READER (+ BABEL-OQ-4 honest-N dose null)
    # =========================================================================================
    if not res["armB"].get("b2_done"):
        gpu_free_check("armB-B2")
        posm=torch.arange(IND_SEG,CERT_BLOCK)
        pp_clean=onset_perpos(None,None)                                       # [N,447]
        M_clean=float(pp_clean.mean())
        # v_onset (L5 verbatim construction)
        posrange=torch.arange(IND_SEG,CERT_BLOCK-1)
        Xc6=(capR[bb].to('cuda')-mu_g[bb]).reshape(N_R,CERT_BLOCK,d)[:,posrange,:].reshape(-1,d)
        probs=pp_clean.reshape(-1).to('cuda')
        k_sel=max(1,int(0.25*probs.numel()))
        hi=torch.topk(probs,k_sel).indices; lo=torch.topk(-probs,k_sel).indices
        v_raw=(Xc6[hi].mean(0)-Xc6[lo].mean(0)); nat_mag=float(v_raw.norm())
        v_onset=v_raw/v_raw.norm().clamp(min=1e-6)
        def onset_dir_delta(sign,mag):
            dv=(sign*mag*v_onset).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous()
            dv=dv.clone(); dv[:, :IND_SEG, :]=0.0; return dv
        # ---- GB-2: v_onset validity replay (A at nat_mag + monotone about M_clean) ----
        if "gb2" not in res["armB"]:
            Mp=onset_mean(injR,onset_dir_delta(+1.0,nat_mag)); Mm=onset_mean(injR,onset_dir_delta(-1.0,nat_mag))
            A_v=(Mp-Mm)/2.0
            mono=bool((Mp-M_clean)*(M_clean-Mm)>0)
            devA=abs(A_v-GB2_A); devM=abs(M_clean-GB2_MCLEAN)
            gb2_ok=bool(devA<=TOL_REPLAY and devM<=TOL_REPLAY and mono)
            res["armB"]["gb2"]={"A":round(A_v,5),"banked_A":GB2_A,"dev_A":round(devA,6),
                "M_clean":round(M_clean,5),"banked_Mclean":GB2_MCLEAN,"dev_M":round(devM,6),
                "M_plus":round(Mp,5),"M_minus":round(Mm,5),"nat_mag":round(nat_mag,4),
                "monotone":mono,"pass":gb2_ok}
            if not gb2_ok and not SMOKE: flag("armB","GB-2_vonset_replay",res["armB"]["gb2"])
            write_json(); logln(f"[GB-2] A={A_v:.5f} (banked {GB2_A}) Mclean={M_clean:.5f} mono={mono} "
                                f"-> {'PASS' if gb2_ok else 'FAIL'}")
        b2_flagged=(not res["armB"]["gb2"]["pass"]) or b1_flagged
        # ---- GEOMETRY (report) ----
        with torch.no_grad():
            Wlast=rung.w.weight[:, -1]                                          # [768] the s-column
        w_s=proj_compl((Wlast/scs.reshape(-1)[-1]).unsqueeze(0)).squeeze(0); w_s=w_s/w_s.norm().clamp(min=1e-6)
        cos_v_img=float(v_onset@rung_img_dir); cos_v_ws=float(v_onset@w_s)
        span5_frac=float((v_onset@span5).norm())
        c_frac=float((v_onset@C_g).norm())
        cos_img_ws=float(rung_img_dir@w_s)
        res["armB"]["b2_geometry"]={"cos_vonset_rungimg":round(cos_v_img,4),
            "cos_vonset_ws":round(cos_v_ws,4),"cos_rungimg_ws":round(cos_img_ws,4),
            "proj_span5_frac":round(span5_frac,4),"proj_C_norm":round(c_frac,4),"nat_mag":round(nat_mag,4)}
        write_json()
        # ---- READER-VALIDITY GATE ----
        if "b2_reader" not in res["armB"]:
            r_p=(oh_real@rung_img_dir).reshape(N_R,CERT_BLOCK)[:,IND_SEG:CERT_BLOCK-1].cpu()   # [N,447]
            r_val=pearson(r_p,pp_clean)
            gcpu=torch.Generator().manual_seed(SEED_B2)
            r_nulls=[]
            for _ in range(N_NULL_B):
                perm=torch.randperm(r_p.shape[1],generator=gcpu)
                r_nulls.append(abs(pearson(r_p[:,perm],pp_clean)))
            rn95=pct95(r_nulls)
            reader_valid=bool(abs(r_val)>=0.3 and abs(r_val)>rn95)
            res["armB"]["b2_reader"]={"pearson_r":round(r_val,4),"null95_shuffle":round(rn95,4),
                "n_shuffles":N_NULL_B,"reader_valid":reader_valid,
                "fbD":(None if reader_valid else "READER-VALIDITY FAILED -> RUNG-IS-READER unavailable")}
            write_json(); logln(f"[B2 reader] r={r_val:.4f} null95={rn95:.4f} -> valid={reader_valid}")
        reader_valid=res["armB"]["b2_reader"]["reader_valid"]
        # ---- CONTROL-WRITES-RUNG-CHANNEL ----
        if "b2_writes" not in res["armB"]:
            WANT2=[7] if SMOKE else [7,8,9]
            sd_rung={}
            for b_ in WANT2:
                Xb=(capR[b_].to('cuda')-mu_g[b_]).reshape(N_R,CERT_BLOCK,d)[:,posm,:].reshape(-1,d)
                sd_rung[b_]=float((Xb@rung_img_dir).std().clamp(min=1e-9)); del Xb
            cP=capture_under_delta(idsR,injR,onset_dir_delta(+1.0,nat_mag),WANT2)
            cM=capture_under_delta(idsR,injR,onset_dir_delta(-1.0,nat_mag),WANT2)
            carry_coord=nat_mag*cos_v_img
            zb={}; zb_cs={}; seb={}
            for b_ in WANT2:
                D_=((cP[b_]-cM[b_])/2.0).to('cuda').reshape(N_R,CERT_BLOCK,d)[:,posm,:]
                co=(D_.reshape(-1,d)@rung_img_dir)
                blk=co.reshape(N_R,-1).mean(1)
                m_=float(co.mean()); se_=float(blk.std(unbiased=True)/math.sqrt(N_R))
                zb[b_]=m_/sd_rung[b_]; zb_cs[b_]=(m_-carry_coord)/sd_rung[b_]; seb[b_]=se_/sd_rung[b_]
                del D_,co
            bstar=max(zb,key=lambda b_:abs(zb[b_])); zmax=abs(zb[bstar])
            # null: matched-magnitude random dirs, same max-over-b statistic (with carry, own random carry)
            gpB2=torch.Generator(device='cuda').manual_seed(SEED_B2)
            nmax=[]
            for it in range(N_NULL_B):
                r=torch.randn(d,generator=gpB2,device='cuda'); r=r/r.norm().clamp(min=1e-6)
                dp=(nat_mag*r).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous(); dp=dp.clone(); dp[:, :IND_SEG, :]=0.0
                dm=(-nat_mag*r).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous(); dm=dm.clone(); dm[:, :IND_SEG, :]=0.0
                nP=capture_under_delta(idsR,injR,dp,WANT2); nM=capture_under_delta(idsR,injR,dm,WANT2)
                mx=0.0
                for b_ in WANT2:
                    D_=((nP[b_]-nM[b_])/2.0).to('cuda').reshape(N_R,CERT_BLOCK,d)[:,posm,:]
                    mx=max(mx,abs(float((D_.reshape(-1,d)@rung_img_dir).mean()))/sd_rung[b_]); del D_
                nmax.append(mx); del nP,nM
                logln(f"[B2 write-null {it+1}/{N_NULL_B}] max|z|={mx:.4f}")
            n95=pct95(nmax)
            control_writes=bool(zmax>n95 and abs(zb[bstar])>=2*seb[bstar])
            res["armB"]["b2_writes"]={"bounds":WANT2,"z_by_b":{str(b_):round(zb[b_],4) for b_ in WANT2},
                "z_carry_subtracted_by_b":{str(b_):round(zb_cs[b_],4) for b_ in WANT2},
                "carry_coord_along_rungimg":round(carry_coord,4),"se_z_by_b":{str(b_):round(seb[b_],5) for b_ in WANT2},
                "b_star":bstar,"z_max":round(zmax,4),"null95":round(n95,4),"n_null":N_NULL_B,
                "control_writes_rung_channel":control_writes}
            write_json(); logln(f"[B2 writes] zmax={zmax:.4f} @b{bstar} null95={n95:.4f} -> {control_writes}")
            del cP,cM; free()
        control_writes=res["armB"]["b2_writes"]["control_writes_rung_channel"]
        # ---- COWRITER TEST (BABEL-OQ-4, honest N=20 at mag6) ----
        if "b2_cowriter" not in res["armB"]:
            dv6,mag6=rung_edit_delta(6); dvm6,_=rung_edit_delta(-6)
            Mp6=onset_mean(injR,dv6); Mm6=onset_mean(injR,dvm6)
            A_on6=(Mp6-Mm6)/2.0
            dev6=abs(A_on6-L5_AON6)
            gpQ=torch.Generator(device='cuda').manual_seed(SEED_OQ4)
            def onset_null(mag,n):
                vals=[]
                for it in range(n):
                    r=torch.randn(d,generator=gpQ,device='cuda'); r=r/r.norm().clamp(min=1e-6)
                    dp=(mag*r).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous(); dp=dp.clone(); dp[:, :IND_SEG, :]=0.0
                    dm=(-mag*r).view(1,1,d).expand(N_R,CERT_BLOCK,d).contiguous(); dm=dm.clone(); dm[:, :IND_SEG, :]=0.0
                    vals.append(abs((onset_mean(injR,dp)-onset_mean(injR,dm))/2.0))
                    logln(f"[OQ4 null mag={mag:.2f} {it+1}/{n}] |A|={vals[-1]:.5f}")
                return vals
            nulls6=onset_null(mag6,N_NULL_OQ4)
            null95_6=pct95(nulls6)
            cowriter=bool(abs(A_on6)>null95_6 and (A_on6*A_on>0))
            nulls3=onset_null(mag3,N_NULL_OQ4)                                  # report-only re-arm of +/-3
            null95_3=pct95(nulls3)
            res["armB"]["b2_cowriter"]={"A_on6":round(A_on6,5),"banked_A_on6":L5_AON6,"replay_dev":round(dev6,6),
                "mag6":round(mag6,4),"null95_20_mag6":round(null95_6,5),
                "nulls_mag6":[round(x,5) for x in nulls6],"n_null":N_NULL_OQ4,
                "sign_matches_Aon":bool(A_on6*A_on>0),"COWRITER":cowriter,
                "report_only_mag3":{"A_on":A_on,"null95_20_mag3":round(null95_3,5),
                    "beats":bool(abs(A_on)>null95_3),
                    "note":"L5 +/-3 verdict stands either way; honest-N re-arm can only sharpen"}}
            write_json(); logln(f"[OQ-4] A_on6={A_on6:.5f} null95_20={null95_6:.5f} -> COWRITER={cowriter} "
                                f"| mag3 rearm: |A_on|={abs(A_on):.5f} vs {null95_3:.5f}")
        cowriter=res["armB"]["b2_cowriter"]["COWRITER"]
        # ---- B2 verdict (mechanical precedence) ----
        if cowriter: v2="RUNG-IS-COWRITER"
        elif reader_valid and control_writes: v2="RUNG-IS-READER"
        else: v2="INDEPENDENT"
        res["armB"]["b2_verdict"]={"cowriter":cowriter,"reader_valid":reader_valid,
            "control_writes":control_writes,"H_L6_B2":v2,
            "bet":"READER45/INDEPENDENT30/COWRITER25","bet_favorite_hit":bool(v2=="RUNG-IS-READER"),
            "instrument_flagged":b2_flagged}
        res["armB"]["b2_done"]=True; write_json()
        logln(f"[B2 VERDICT] cowriter={cowriter} reader_valid={reader_valid} writes={control_writes} -> {v2}")
        del Xc6,probs; free()

    # =========================================================================================
    # B3 -- corr_j17 LEAKAGE vs GENUINE (echo decomposition; L4 T3 machinery byte-verbatim)
    # =========================================================================================
    if not res["armB"].get("b3_done"):
        gpu_free_check("armB-B3")
        idsC,capC,YclC=get_regime("code"); N_C=idsC.shape[0]
        v17=Q35_g[:,17]; v17=v17/v17.norm().clamp(min=1e-6)
        coordC=(capC[5].to('cuda')-mu_g[5])@v17; sigC=float(coordC.std())
        # L4 T3 readout battery (5 columns, same construction order)
        RD_DEFS=[("naval",C_g[:,0]),("clause",Q35_g[:,4]),("operator",v17),("symbol",C_g[:,2]),("rung",rung_img_dir)]
        readouts=[]; rd_names=[]
        for (nm,vec) in RD_DEFS:
            v=vec/vec.norm().clamp(min=1e-6); readouts.append(wu_image(v)); rd_names.append(nm)
        own=rd_names.index("operator")
        injB5=InjectHook(M["blocks"][4]); injB12=InjectHook(M["blocks"][11])
        pos_lo,pos_hi=0,CERT_BLOCK
        if "b3_decomp" not in res["armB"]:
            KS=[3,-3] if SMOKE else [3,-3,6,-6]
            kcA={}; kcD={}
            for k in KS:
                dv=((k*sigC)*v17).view(1,1,d).expand(N_C,CERT_BLOCK,d).contiguous()
                kcA[k]=logits_under_delta(idsC,injB5,dv,readouts,pos_lo,pos_hi)
                kcD[k]=logits_under_delta(idsC,injB12,dv,readouts,pos_lo,pos_hi)
                logln(f"[B3 k={k}] own full={kcA[k][own]:.4f} direct={kcD[k][own]:.4f}")
            M3_full_row={rd_names[j]:round((kcA[3][j]-kcA[-3][j])/2.0,4) for j in range(len(readouts))}
            Mii_full=(kcA[3][own]-kcA[-3][own])/2.0
            M_direct=(kcD[3][own]-kcD[-3][own])/2.0
            M_comp=Mii_full-M_direct
            if 6 in kcA:
                M6_full=(kcA[6][own]-kcA[-6][own])/2.0; M6_direct=(kcD[6][own]-kcD[-6][own])/2.0
                M6_comp=M6_full-M6_direct
            else: M6_full=M6_direct=M6_comp=None
            devMii=abs(Mii_full-GB3_MII); gb3_ok=bool(devMii<=TOL_REPLAY)
            if not gb3_ok and not SMOKE: flag("armB","GB-3_j17_replay",f"Mii={Mii_full} banked={GB3_MII} dev={devMii}")
            res["armB"]["b3_decomp"]={"sigma_code_b5":round(sigC,4),"banked_sigma":L4_SIG_J17,
                "M3_full_row":M3_full_row,"Mii_full":round(Mii_full,4),"banked_Mii":GB3_MII,
                "gb3_dev":round(devMii,6),"gb3_pass":gb3_ok,
                "M_direct":round(M_direct,4),"M_comp":round(M_comp,4),
                "M6_full":(round(M6_full,4) if M6_full is not None else None),"banked_M6":GB3_M6,
                "M6_direct":(round(M6_direct,4) if M6_direct is not None else None),
                "M6_comp":(round(M6_comp,4) if M6_comp is not None else None)}
            write_json(); logln(f"[GB-3] Mii={Mii_full:.4f} (banked {GB3_MII}) -> {'PASS' if gb3_ok else 'FAIL'} "
                                f"| direct={M_direct:.4f} comp={M_comp:.4f}")
        dec=res["armB"]["b3_decomp"]
        b3_flagged=not dec["gb3_pass"]
        # ---- nulls for computed + direct legs ----
        if "b3_null" not in res["armB"]:
            gpB3=torch.Generator(device='cuda').manual_seed(SEED_B3)
            mag3C=3*sigC
            comp_n=[]; dir_n=[]
            for it in range(N_NULL_B):
                r=torch.randn(d,generator=gpB3,device='cuda'); r=r/r.norm().clamp(min=1e-6)
                dp=(mag3C*r).view(1,1,d).expand(N_C,CERT_BLOCK,d).contiguous()
                dm=(-mag3C*r).view(1,1,d).expand(N_C,CERT_BLOCK,d).contiguous()
                fA=(logits_under_delta(idsC,injB5,dp,[readouts[own]],pos_lo,pos_hi)[0]
                    -logits_under_delta(idsC,injB5,dm,[readouts[own]],pos_lo,pos_hi)[0])/2.0
                fD=(logits_under_delta(idsC,injB12,dp,[readouts[own]],pos_lo,pos_hi)[0]
                    -logits_under_delta(idsC,injB12,dm,[readouts[own]],pos_lo,pos_hi)[0])/2.0
                comp_n.append(abs(fA-fD)); dir_n.append(abs(fD))
                logln(f"[B3 null {it+1}/{N_NULL_B}] |comp|={comp_n[-1]:.4f} |direct|={dir_n[-1]:.4f}")
            res["armB"]["b3_null"]={"null95_comp":round(pct95(comp_n),4),"null95_direct":round(pct95(dir_n),4),
                "n_null":N_NULL_B,"comp_draws":[round(x,4) for x in comp_n],
                "direct_draws":[round(x,4) for x in dir_n],"mag3":round(3*sigC,4)}
            write_json()
        nn_=res["armB"]["b3_null"]; null95_comp=nn_["null95_comp"]; null95_dir=nn_["null95_direct"]
        # ---- bands (mechanical) + echo-sanity FB-D ----
        Mii_full=dec["Mii_full"]; M_direct=dec["M_direct"]; M_comp=dec["M_comp"]; M6_comp=dec["M6_comp"]
        echo_measurable=bool(abs(M_direct)>null95_dir)
        comp_real=bool(abs(M_comp)>null95_comp)
        if not echo_measurable:
            v3_=("GENUINE-ON-MANIFOLD-CONTROL" if (comp_real and M_comp*Mii_full>0
                 and (M6_comp is None or M6_comp*M_comp>0)) else "NOT-GENUINE")
            fbD="echo unmeasurable (|M_direct|<=null95_direct) -> LEAKAGE band unavailable; reduced verdict"
        else:
            fbD=None
            if not comp_real: v3_="LEAKAGE"
            elif abs(M_comp)<abs(M_direct): v3_="MIXED"
            elif (M_comp*Mii_full>0) and (M6_comp is None or M6_comp*M_comp>0): v3_="GENUINE-ON-MANIFOLD-CONTROL"
            else: v3_="MIXED"
        res["armB"]["b3_verdict"]={"echo_measurable":echo_measurable,"comp_beats_null":comp_real,
            "H_L6_B3":v3_,"fbD":fbD,"bet":"MIXED40/LEAKAGE35/GENUINE25",
            "bet_favorite_hit":bool(v3_=="MIXED"),"instrument_flagged":b3_flagged}
        write_json(); logln(f"[B3 VERDICT] comp={M_comp} vs null95 {null95_comp} | direct={M_direct} vs "
                            f"{null95_dir} -> {v3_}")
        # ---- MANIFOLD GEOMETRY + BOUND CONDITIONALITY (report-only texture; FB-C droppable) ----
        if "b3_texture" not in res["armB"] and not SMOKE and el()<SOFT_WALL_S:
            tex={"sigma_b5":{},"m_frac":{},"offspan":{}}
            for regime in REGIMES:
                ids_,cap_,Ycl_=get_regime(regime)
                Xb5=cap_[5].to('cuda')-mu_g[5]
                tex["sigma_b5"][regime]=round(float((Xb5@v17).std()),4)
                U_,S_,Vh_=torch.linalg.svd(Xb5,full_matrices=False)
                mf={}
                for K in (16,64,256):
                    mf[str(K)]=round(float(((Vh_[:K]@v17)**2).sum()),4)
                tex["m_frac"][regime]=mf
                del Xb5,U_,S_,Vh_; free()
            # off-span rows byte-verbatim _l3.py M3 (proj axis; L3 class rules) in prose + repetition
            for regime in ("prose","repetition"):
                ids_,cap_,Ycl_=get_regime(regime)
                N_=ids_.shape[0]
                injO=InjectHook(M["blocks"][4])
                gpO=torch.Generator(device='cuda').manual_seed(SEED_L3_J17)
                Xc_=cap_[5].to('cuda')-mu_g[5]; sd_c=float((Xc_@v17).std())
                nulls=[]
                for _ in range(3):
                    r=torch.randn(d,generator=gpO,device='cuda'); r=r-(r@v17)*v17; r=r/r.norm(); nulls.append(r)
                rows={}
                for k in [3,5,10,-3,-5,-10]:
                    mag=abs(k*sd_c); dvec=(k*sd_c)*v17
                    delta=dvec.view(1,1,d).expand(N_,CERT_BLOCK,d)
                    if regime=="repetition":
                        dz=delta.clone(); dz[:, :IND_SEG, :]=0.0
                        kl_ax=inject_kl_pidx(ids_,injO,dz,Ycl_,torch.arange(IND_SEG,CERT_BLOCK))
                    else:
                        kl_ax=inject_kl_full(ids_,injO,delta,Ycl_)
                    kl_nulls=[]
                    for r in nulls:
                        dn=(mag*r).view(1,1,d).expand(N_,CERT_BLOCK,d)
                        if regime=="repetition":
                            dz2=dn.clone(); dz2[:, :IND_SEG, :]=0.0
                            kl_nulls.append(inject_kl_pidx(ids_,injO,dz2,Ycl_,torch.arange(IND_SEG,CERT_BLOCK)))
                        else:
                            kl_nulls.append(inject_kl_full(ids_,injO,dn,Ycl_))
                    kl_null=sum(kl_nulls)/len(kl_nulls)
                    rows[str(k)]={"kl_axis":round(kl_ax,5),"kl_null":round(kl_null,5),
                                  "R":round(kl_ax/max(kl_null,1e-9),4),"mag":round(mag,4)}
                    logln(f"[B3 offspan {regime} k={k}] R={rows[str(k)]['R']}")
                injO.close()
                R10=(rows["10"]["R"]+rows["-10"]["R"])/2
                cls=("STRUCTURED-EXTRAPOLATION" if R10>=1.5 else
                     ("MANIFOLD-BOUND" if R10>1/1.5 else "SATURATING-OR-NULL"))
                tex["offspan"][regime]={"rows":rows,"R_k10":round(R10,4),"class":cls,"sigma":round(sd_c,4)}
                del Xc_; free()
            tex["offspan"]["code_banked"]={"R_k10":0.8585,"class":"MANIFOLD-BOUND","source":"OFFSPAN_TABLE_V1"}
            res["armB"]["b3_texture"]=tex; write_json()
        injB5.close(); injB12.close()
        res["armB"]["b3_done"]=True; write_json()

    injR.close()

    # =========================================================================================
    # ARM A -- A2 ADJUDICATE (L1 battery byte-verbatim over the selected dark directions)
    # =========================================================================================
    if not res["armA"].get("a2_done"):
        gpu_free_check("armA-A2")
        # ---- battery objects (L1 verbatim: _open1_bases + decoder_v1 + _open4_probe) ----
        o1=torch.load(os.path.join(DIR,"_open1_bases.pt"),map_location="cpu",weights_only=False)
        mu_bat=o1["mu"].float(); B2_batc=o1["B2"].float(); U=o1["U"]
        v1=torch.load(os.path.join(DIR,"decoder_v1_tensors.pt"),map_location="cpu",weights_only=False)
        p4=json.load(open(os.path.join(DIR,"_open4_probe.json"),encoding="utf-8"))
        frozen=[(r["room"],r["dim"]) for r in p4["selection"]["corridor_distinct"]]
        B2_batg=B2_batc.to('cuda'); Pfull=torch.eye(d,device='cuda')
        bat_gates_ok=True
        # G1: M0a-subset content gate
        if not res["gates"].get("G1_M0a_subset"):
            def md(a,b): return float((a.float()-b.float()).abs().max())
            cm={"B2_vs_v1":md(B2_batc,v1["B2"].float()),"mu_vs_v1":md(mu_bat,v1["mu"].float())}
            seen=[]; kept=[]
            for b_ in ROOMS:
                for i in range(16):
                    u=U[b_][:,i].float(); best=0.0
                    for (kb,ki,vv) in seen:
                        dd_=abs(float(u@vv))
                        if dd_>best: best=dd_
                    if best<=0.8: kept.append((b_,i))
                    seen.append((b_,i,u))
            corr_match=bool(kept==frozen)
            g1_ok=(all(v==0.0 for v in cm.values()) and corr_match and len(frozen)==35)
            res["gates"]["G1_M0a_subset"]={"content_match":cm,"corridor_recompute_match":corr_match,
                                           "n_corridor":len(frozen),"pass":bool(g1_ok)}
            write_json(); logln(f"[G1] cm={cm} corr_match={corr_match} -> {'PASS' if g1_ok else 'FAIL'}")
        bat_gates_ok=bat_gates_ok and res["gates"]["G1_M0a_subset"]["pass"]
        V35=torch.stack([U[r_][:,d_].float() for (r_,d_) in frozen],1); V35_g=V35.to('cuda')
        # battery streams (L1 verbatim)
        wt=torch.load(os.path.join(DIR,"_t14_wt103_ids.pt"),map_location="cpu",weights_only=False)
        stand64=ids_window(wt["ids"].tolist(),wt["lo"],wt["lo"]+N_STAND_ANCHOR*CERT_BLOCK,"wt103 standing")[:N_STAND_ANCHOR]
        STREAMS_BAT={"prose":stand64[:N_BANK],"repetition":build_dind(N_BANK,CERT_BLOCK,REP_SEED)}
        CIDS=tok(load_code_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
        STREAMS_BAT["code"]=ids_window(CIDS,FRESH_LO,FRESH_HI,"fresh code")[:N_BANK]
        BAT_REGS=(["prose"] if SMOKE else REGIMES)
        CAPS_BAT={reg:capture_which(STREAMS_BAT[reg],CAP_CHUNK,f"bank-{reg}",which=[6]) for reg in BAT_REGS}
        # G3: snap identity at matched batch shape
        if not res["gates"].get("G3_snap_identity"):
            g3={}
            for reg in BAT_REGS:
                g3[reg]=snap_identity_check(STREAMS_BAT[reg][:4].to('cuda'))
            g3_ok=all(v<=1e-4 for v in g3.values())
            res["gates"]["G3_snap_identity"]={"max_dlogit":g3,"pass":bool(g3_ok)}
            write_json(); logln(f"[G3] {g3} -> {'PASS' if g3_ok else 'FAIL'}")
        bat_gates_ok=bat_gates_ok and res["gates"]["G3_snap_identity"]["pass"]
        # G4: corridor anchor replay (j0, j16)
        if not res["gates"].get("G4_anchor_replay"):
            anch_bounds=sorted({frozen[j][0] for j in [0,16]})
            Hs64=capture_which(stand64,CAP_CHUNK,"anchor-stand64",which=anch_bounds)
            idg64=stand64.to('cuda')
            g4recs={}; g4_ok=True
            for j in [0,16]:
                rm,dm_=frozen[j]; vdir=V35_g[:,j]
                col=wte_g@(vdir*lnf_gpu); top=torch.topk(col,40).indices; bot=torch.topk(-col,40).indices
                a=(Hs64[rm].to('cuda')-mu_bat[rm].to('cuda'))@vdir; sigma=float(a.std())
                flatidx=torch.topk(a.abs(),16).indices.tolist()
                seqs=[t//CERT_BLOCK for t in flatidx]; rows=torch.tensor(seqs,dtype=torch.long,device='cuda')
                ids_b=idg64[rows]; nP=len(flatidx)
                snap=[SnapHook(M["blocks"][L].attn,True) for L in range(nL)]
                ones=torch.ones(nP,CERT_BLOCK,device='cuda'); capb=[rm-1,rm]
                base,_=measure_class_snap_cap(M["m"],snap,ids_b,Pfull,vdir.contiguous(),ones,[top,bot],MB,capb)
                delt=torch.zeros(nP,2,2)
                for si,s_ in enumerate([1.0,-1.0]):
                    fac=torch.ones(nP,CERT_BLOCK,device='cuda')
                    for r_,t_ in enumerate(flatidx):
                        a0=float(a[t_]); pos=t_%CERT_BLOCK
                        if abs(a0)>=A_EPS: fac[r_,pos]=(a0+s_*sigma)/a0
                    mod_,_=measure_class_snap_cap(M["m"],snap,ids_b,Pfull,vdir.contiguous(),fac,[top,bot],MB,capb)
                    for r_,t_ in enumerate(flatidx):
                        pos=t_%CERT_BLOCK; delt[r_,si]=mod_[r_,pos]-base[r_,pos]
                for h in snap: h.close()
                dT=(delt[:,0,0]-delt[:,1,0])/2.0; dB=(delt[:,0,1]-delt[:,1,1])/2.0
                Cv=float((dT-dB).mean()); dev=abs(Cv-C_BANKED[j]["C"])
                ok=bool(dev<=TOL_ANCHOR)
                g4recs[f"j{j}"]={"C":round(Cv,5),"banked":C_BANKED[j]["C"],"dev":round(dev,5),"pass":ok}
                g4_ok=g4_ok and ok
                logln(f"[G4 j={j}] C={Cv:.5f} banked={C_BANKED[j]['C']} dev={dev:.5f} -> {'PASS' if ok else 'FAIL'}")
            del Hs64
            res["gates"]["G4_anchor_replay"]={"anchors":g4recs,"pass":bool(g4_ok)}; write_json()
        bat_gates_ok=bat_gates_ok and res["gates"]["G4_anchor_replay"]["pass"]
        res["gates"]["G2_G5_omitted"]="fold-provenance gates NOT carried (L6 consumes no fold bases) -- FLAGGED per pre-reg"
        if not bat_gates_ok:
            flag("armA-A2","GA-2_battery_gates","G1/G3/G4 not all PASS -> A2 adjudication instrument-void (FB-B)")
        # ---- word_battery (V4/_l1.py machinery byte-verbatim; adapted names only) ----
        def word_battery(vdir_g,bnd,regime,jseed,bnull,null_orth_q35,tag):
            H=CAPS_BAT[regime][bnd].to('cuda'); ids_full=STREAMS_BAT[regime].to('cuda')
            a=(H-mu_bat[bnd].to('cuda'))@vdir_g; sigma=float(a.std())
            col=wte_g@(vdir_g*lnf_gpu); top=torch.topk(col,40).indices; bot=torch.topk(-col,40).indices
            class_idx=[top,bot]
            Wtop=wte_cpu[top.cpu()]; Wbot=wte_cpu[bot.cpu()]
            int_blocks=[x for x in (bnd,bnd+1,bnd+2) if x<=nL-1]
            capb=sorted(set([bnd-1]+([bnd] if bnd<=nL-1 else [])+int_blocks))
            has_field=bnd<=nL-1
            flatidx=torch.topk(a.abs(),16).indices.tolist()
            seqs=[t//CERT_BLOCK for t in flatidx]; rows=torch.tensor(seqs,dtype=torch.long,device='cuda')
            ids_b=ids_full[rows]; nP=len(flatidx)
            snap=[SnapHook(M["blocks"][L].attn,True) for L in range(nL)]
            ci=vdir_g.contiguous(); vcpu=vdir_g.cpu()
            ones=torch.ones(nP,CERT_BLOCK,device='cuda')
            base,cap0=measure_class_snap_cap(M["m"],snap,ids_b,Pfull,ci,ones,class_idx,MB,capb)
            def push(mag):
                delt=torch.zeros(nP,2,2); Dvec={}; INTd={k:{} for k in int_blocks}
                for si,s_ in enumerate([1.0,-1.0]):
                    fac=torch.ones(nP,CERT_BLOCK,device='cuda')
                    for r_,t_ in enumerate(flatidx):
                        a0=float(a[t_]); pos=t_%CERT_BLOCK
                        if abs(a0)>=A_EPS: fac[r_,pos]=(a0+s_*mag*sigma)/a0
                    mod_,capm=measure_class_snap_cap(M["m"],snap,ids_b,Pfull,ci,fac,class_idx,MB,capb)
                    dvs=[]; intd={k:[] for k in int_blocks}
                    for r_,t_ in enumerate(flatidx):
                        pos=t_%CERT_BLOCK; delt[r_,si]=mod_[r_,pos]-base[r_,pos]
                        if has_field:
                            d_lo=capm[bnd-1].reshape(nP,CERT_BLOCK,d)[r_,pos]-cap0[bnd-1].reshape(nP,CERT_BLOCK,d)[r_,pos]
                            d_hi=capm[bnd].reshape(nP,CERT_BLOCK,d)[r_,pos]-cap0[bnd].reshape(nP,CERT_BLOCK,d)[r_,pos]
                            dc=(d_hi-d_lo); dc=dc-(dc@vcpu)*vcpu; dvs.append(dc)
                        for k in int_blocks:
                            dk=capm[k].reshape(nP,CERT_BLOCK,d)[r_,pos]-cap0[k].reshape(nP,CERT_BLOCK,d)[r_,pos]
                            intd[k].append(dk)
                    if has_field: Dvec[si]=torch.stack(dvs,0)@B2_batc
                    for k in int_blocks: INTd[k][si]=torch.stack(intd[k],0)
                dT=(delt[:,0,0]-delt[:,1,0])/2.0; dB=(delt[:,0,1]-delt[:,1,1])/2.0
                cp=(dT-dB); C_=float(cp.mean()); SE=float(cp.std(unbiased=True)/math.sqrt(nP))
                fld=None
                if has_field:
                    Dp=Dvec[0].mean(0); Dm=Dvec[1].mean(0)
                    fld={"cos":float((Dp@Dm)/max(1e-12,float(Dp.norm())*float(Dm.norm()))),
                         "Dmag":float((Dp-Dm).norm()/2.0),"Dp":Dp,"Dm":Dm}
                ints={}
                for k in int_blocks:
                    dk=(INTd[k][0]-INTd[k][1])/2.0
                    dkl=dk*lnf_cpu
                    ct=(dkl@Wtop.t()).mean(-1)-(dkl@Wbot.t()).mean(-1)
                    ints[k+1]={"C":float(ct.mean()),"SE":float(ct.std(unbiased=True)/math.sqrt(nP))}
                return {"C":C_,"SE":SE,"field":fld,"int":ints}
            r1=push(1.0); r2=push(2.0)
            null_C=[]; null_D=[]; null_INT=[]
            for it in range(bnull):
                Rr=torch.randn(d,generator=torch.Generator().manual_seed(9000+jseed*100+it)).to('cuda')
                Rr=Rr-B2_batg@(B2_batg.t()@Rr)
                if null_orth_q35: Rr=Rr-Q35_g@(Q35_g.t()@Rr)
                Rr=Rr/Rr.norm().clamp(min=1e-9)
                colr=wte_g@(Rr*lnf_gpu); topr=torch.topk(colr,40).indices; botr=torch.topk(-colr,40).indices
                Wtopr=wte_cpu[topr.cpu()]; Wbotr=wte_cpu[botr.cpu()]
                ar=(H-mu_bat[bnd].to('cuda'))@Rr
                fi=torch.topk(ar.abs(),16).indices.tolist(); sq=[t//CERT_BLOCK for t in fi]
                rowsn=torch.tensor(sq,dtype=torch.long,device='cuda'); ids_n=ids_full[rowsn]
                cir=Rr.contiguous(); rcpu=Rr.cpu()
                onesn=torch.ones(len(fi),CERT_BLOCK,device='cuda')
                basen,cap0n=measure_class_snap_cap(M["m"],snap,ids_n,Pfull,cir,onesn,[topr,botr],MB,capb)
                dl=torch.zeros(len(fi),2,2); Dv={}; INTn={k:{} for k in int_blocks}
                for si,s_ in enumerate([1.0,-1.0]):
                    fac=torch.ones(len(fi),CERT_BLOCK,device='cuda')
                    for r_,t_ in enumerate(fi):
                        a0=float(ar[t_]); pos=t_%CERT_BLOCK
                        if abs(a0)>=A_EPS: fac[r_,pos]=(a0+s_*sigma)/a0
                    mod_,capm=measure_class_snap_cap(M["m"],snap,ids_n,Pfull,cir,fac,[topr,botr],MB,capb)
                    dvs=[]; intd={k:[] for k in int_blocks}
                    for r_,t_ in enumerate(fi):
                        pos=t_%CERT_BLOCK; dl[r_,si]=mod_[r_,pos]-basen[r_,pos]
                        if has_field:
                            d_lo=capm[bnd-1].reshape(len(fi),CERT_BLOCK,d)[r_,pos]-cap0n[bnd-1].reshape(len(fi),CERT_BLOCK,d)[r_,pos]
                            d_hi=capm[bnd].reshape(len(fi),CERT_BLOCK,d)[r_,pos]-cap0n[bnd].reshape(len(fi),CERT_BLOCK,d)[r_,pos]
                            dc=(d_hi-d_lo); dc=dc-(dc@rcpu)*rcpu; dvs.append(dc)
                        for k in int_blocks:
                            dk=capm[k].reshape(len(fi),CERT_BLOCK,d)[r_,pos]-cap0n[k].reshape(len(fi),CERT_BLOCK,d)[r_,pos]
                            intd[k].append(dk)
                    if has_field: Dv[si]=torch.stack(dvs,0)@B2_batc
                    for k in int_blocks: INTn[k][si]=torch.stack(intd[k],0)
                dTn=(dl[:,0,0]-dl[:,1,0])/2.0; dBn=(dl[:,0,1]-dl[:,1,1])/2.0
                null_C.append(abs(float((dTn-dBn).mean())))
                if has_field: null_D.append(float((Dv[0].mean(0)-Dv[1].mean(0)).norm()/2.0))
                mx=0.0
                for k in int_blocks:
                    dk=(INTn[k][0]-INTn[k][1])/2.0
                    dkl=dk*lnf_cpu
                    ct=(dkl@Wtopr.t()).mean(-1)-(dkl@Wbotr.t()).mean(-1)
                    mx=max(mx,abs(float(ct.mean())))
                null_INT.append(mx)
            for h in snap: h.close()
            null95C=pct95(null_C); null95D=pct95(null_D) if null_D else None; null95I=pct95(null_INT) if null_INT else None
            wu_clear=bool(abs(r1["C"])>null95C and abs(r1["C"])>=2*r1["SE"])
            wu_stable=bool(wu_clear and (r1["C"]*r2["C"]>0) and abs(r2["C"])>=2*r2["SE"])
            int_clear=False; int_stable=False; kstar=None; mxi1=0.0
            if r1["int"]:
                kstar=max(r1["int"],key=lambda k:abs(r1["int"][k]["C"])); mxi1=abs(r1["int"][kstar]["C"])
                i1=r1["int"][kstar]; i2=r2["int"][kstar]
                int_clear=bool(mxi1>(null95I or float("inf")) and abs(i1["C"])>=2*i1["SE"])
                int_stable=bool(int_clear and (i1["C"]*i2["C"]>0) and abs(i2["C"])>=2*i2["SE"])
            field_clear=False; field_stable=False
            if r1["field"] is not None:
                field_clear=bool(r1["field"]["cos"]<=-0.5 and r1["field"]["Dmag"]>(null95D or float("inf")))
                field_stable=bool(field_clear and r2["field"]["cos"]<=-0.5)
            stable=bool(wu_stable or int_stable or field_stable)
            n_clear=int(wu_clear)+int(int_clear)+int(field_clear)
            posh=[int(t%CERT_BLOCK) for t in flatidx]
            wte_side=(wte_cpu@vcpu)
            wtop=[tok.decode([i]) for i in torch.topk(wte_side,10).indices.tolist()]
            wbot=[tok.decode([i]) for i in torch.topk(-wte_side,10).indices.tolist()]
            cur=[tok.decode([int(ids_full[t//CERT_BLOCK,t%CERT_BLOCK])]) for t in flatidx[:8]]
            wu_top=[tok.decode([i]) for i in top[:10].tolist()]
            wu_bot=[tok.decode([i]) for i in bot[:10].tolist()]
            rec={"sigma":round(sigma,4),"n_null":bnull,
                 "C1":round(r1["C"],4),"SE1":round(r1["SE"],4),"C2":round(r2["C"],4),"SE2":round(r2["SE"],4),
                 "null95_C":round(null95C,4),"wu_clear":wu_clear,"wu_stable":wu_stable,
                 "int1":{str(k):{"C":round(v_["C"],4),"SE":round(v_["SE"],4)} for k,v_ in r1["int"].items()},
                 "int2":{str(k):{"C":round(v_["C"],4),"SE":round(v_["SE"],4)} for k,v_ in r2["int"].items()},
                 "int_kstar":(int(kstar) if kstar is not None else None),"maxint1":round(mxi1,4),
                 "null95_INT":(round(null95I,4) if null95I is not None else None),
                 "int_clear":int_clear,"int_stable":int_stable,
                 "field":({"cos1":round(r1["field"]["cos"],4),"cos2":round(r2["field"]["cos"],4),
                           "Dmag1":round(r1["field"]["Dmag"],4),"Dmag2":round(r2["field"]["Dmag"],4),
                           "null95_D":(round(null95D,4) if null95D is not None else None)}
                          if r1["field"] is not None else None),
                 "field_clear":field_clear,"field_stable":field_stable,
                 "stable":stable,"n_channels_clear":n_clear,
                 "pos":{"pos16":posh,"wte_top":wtop,"wte_bot":wbot,"cur_tokens":cur,
                        "wu_top":wu_top,"wu_bot":wu_bot}}
            del H
            return rec
        # ---- adjudicate selected directions (cap 8; DIFFUSE -> top-8 SVD; jseed=300+i) ----
        Vsel_c=BASES.get("armA_selected_dirs")
        if Vsel_c is None: raise RuntimeError("selected dirs missing from BASES")
        n_sel_total=Vsel_c.shape[1]
        n_adj=min(BATTERY_CAP,n_sel_total)
        res["armA"].setdefault("a2_words",{})
        if bat_gates_ok:
            for i in range(n_adj):
                wid=f"dark_b6_svd{i}"
                if res["armA"]["a2_words"].get(wid,{}).get("done"): continue
                if el()>HARD_WALL_S:
                    logln(f"[FB-WALL] hard wall at {wid}; remaining UNADJUDICATED"); break
                tw0=time.time()
                vdir_g=Vsel_c[:,i].to('cuda').contiguous()
                regs={}
                for regime in BAT_REGS:
                    regs[regime]=word_battery(vdir_g,6,regime,300+i,B_NULL_BAT,True,wid)
                n_stable=sum(1 for r_ in regs.values() if r_["stable"])
                stable_regs=[rg_ for rg_ in BAT_REGS if regs[rg_]["stable"]]
                verdict="CERTIFIED-NO-GLOSS"
                if n_stable>=2: verdict="NAMED"
                elif n_stable==1 and stable_regs[0]=="prose" and regs["prose"]["n_channels_clear"]>=2:
                    verdict="NAMED-REGIME-SPECIFIC"
                res["armA"]["a2_words"][wid]={"done":True,"dir_index":i,"regimes":regs,
                    "n_regimes_stable":n_stable,"stable_regimes":stable_regs,"verdict":verdict,
                    "t_s":round(time.time()-tw0,1)}
                write_json(); save_bases()
                logln(f"[A2 {wid}] stable={stable_regs} verdict={verdict} ({res['armA']['a2_words'][wid]['t_s']}s; "
                      f"{i+1}/{n_adj})")
                free()
        # ---- A2 verdict ----
        words=res["armA"]["a2_words"]
        done_w={k:v for k,v in words.items() if v.get("done")}
        n_done=len(done_w)
        n_named=sum(1 for v in done_w.values() if v["verdict"].startswith("NAMED"))
        f_named=(n_named/n_done) if n_done else None
        if not bat_gates_ok or n_done==0:
            band2="INSTRUMENT-VOID" if not bat_gates_ok else "UNADJUDICATED"
        elif f_named==0: band2="ALL-DARK"
        elif f_named<0.5: band2="NAMED-SOME"
        else: band2="NAMED-MAJORITY"
        res["armA"]["a2_verdict"]={"n_selected_total":n_sel_total,"n_adjudicated":n_done,
            "n_unadjudicated":max(0,n_sel_total-n_done),"n_named":n_named,
            "f_named":(round(f_named,3) if f_named is not None else None),"H_L6_A2":band2,
            "battery_gates_pass":bat_gates_ok,
            "bet":"ALLDARK45/SOME35/MAJORITY20","bet_favorite_hit":bool(band2=="ALL-DARK"),
            "lexicon_v4_trigger":bool(n_named>0)}
        res["armA"]["a2_done"]=True; write_json()
        logln(f"[A2 VERDICT] named {n_named}/{n_done} -> {band2}")

    # ================= VERDICT ASSEMBLY + STATUS =================
    res["verdicts"]={
        "H_L6_A1":res["armA"].get("a1_verdict",{}).get("H_L6_A1"),
        "A3_gate":res["armA"].get("a3",{}).get("verdict_text"),
        "H_L6_A2":res["armA"].get("a2_verdict",{}).get("H_L6_A2"),
        "H_L6_B1":res["armB"].get("b1",{}).get("H_L6_B1"),
        "H_L6_B2":res["armB"].get("b2_verdict",{}).get("H_L6_B2"),
        "H_L6_B3":res["armB"].get("b3_verdict",{}).get("H_L6_B3")}
    if SMOKE:
        okA=bool(res["armA"].get("a1_done") and res["armA"].get("a2_done"))
        okB=bool(res["armB"].get("b1_done") and res["armB"].get("b2_done") and res["armB"].get("b3_done"))
        res["status"]="SMOKE-"+("OK" if (okA and okB) else "FAIL")
    else:
        done=(res["armA"].get("a1_done") and res["armA"].get("a2_done")
              and res["armB"].get("b1_done") and res["armB"].get("b2_done") and res["armB"].get("b3_done"))
        res["status"]=("COMPLETE" if (done and not res["instrument_discrepancy"]) else
                       ("COMPLETE-WITH-DISCREPANCY" if done else "PARTIAL"))
    BASES["verdicts"]=res["verdicts"]
    save_bases(); write_json()
    if M["m"] is not None: del M["m"]; M["m"]=None; free()
except Exception as e:
    res["fatal_error"]={"error":str(e),"trace":traceback.format_exc()}
    logln(f"FATAL {e}\n{traceback.format_exc()}"); res.setdefault("status","FATAL")
write_json()
logln(f"L6 END status={res.get('status')} elapsed={el()}s verdicts={res.get('verdicts')}")
open(os.path.join(DIR,"_l6_smoke_gpu.done" if SMOKE else "_l6_gpu.done"),"w").write(str(res.get("status","?"))+"\n")
logln("*** L6_"+("SMOKE_" if SMOKE else "")+"DONE ***"); LOG.flush(); LOG.close(); print("done")
