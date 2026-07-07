# _v7.py -- V7 THE FINISH-LINE RUN (code-column fold + onset surrogate + asterisk discharge). GPT-2 124M. PROPOSE-ONLY.
# Pre-registration: FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md ::
#   "V7 -- THE FINISH-LINE RUN ... GAP-SCAN + PRE-REGISTRATION (2026-07-05 ~22:35)"
# Brief: V7_BRIEF_2026-07-05.md (Will "run it all in sequence"). Doctrine: plan binding, propose-only,
#   bands SHARPENED never weakened, escalation binding, both-meter reporting permanent, recal PRIMARY.
# MACHINERY reused VERBATIM from _v6.py: model loader / capture / KL / InjectHook / inject_kl_full /
#   inject_kl_pidx / write_svd / load_objects+M0a gate / s4_delta / Arm-B folded-r48 recipe /
#   surrogate rung classes + MSE trainer + shuffled twins / substitution cert / behav meter.
# NEW: Arm A = folded r20/r48 at code b4..b11 + prose_b12 (3-regime Gram recipe verbatim, replay
#   gates per pre-reg); Arm B = onset surrogate at BUS[6]/BUS[7] with locked contracts CT-A/CT-B/
#   (CT-C conditional), linear-first ladder; Arm C1 = frozen decoder_v6 across 5 fresh batches;
#   Arm C2 = front-door ablation retrain; verdict recompute BOTH meters with V7 grain overrides.
import json, time, os, math, traceback, gc, subprocess, hashlib, ctypes
import torch, torch.nn as nn, torch.nn.functional as Fnn
import torch.nn.functional as F

t0=time.time()
DIR=r"C:\Shadow\Dissector\D0_PROGRAM\CONSTRUCTIVE"
SMOKE=os.environ.get("V7_SMOKE")=="1"
LOG=open(os.path.join(DIR,"_v7.log"),"a",encoding="utf-8")
def logln(s):
    s=str(s); LOG.write(f"[V7 {round(time.time()-t0,1):8.1f}s] "+s+"\n"); LOG.flush()
    try: print(s,flush=True)
    except Exception: pass
def el(): return round(time.time()-t0,1)
logln("="*100); logln(f"V7 START smoke={SMOKE} torch={torch.__version__}")
try:
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(),0x4000)
    logln("[ops] priority BelowNormal set")
except Exception as e: logln(f"[ops] priority set failed: {e}")
torch.set_num_threads(6)

# ---------------- locked constants ----------------
EPS_KL=0.1871; CERT_BLOCK=512; IND_SEG=64; MB=4; CAP_CHUNK=16
VOCAB_SANS_SPECIALS=50256; REGIMES=["prose","code","repetition"]
FRESH_LO,FRESH_HI=24576,32768
REP_SEED=3; SEED_J=20260705
B2b=2; B5=5
# surrogate config (V6 verbatim where shared)
MLP_H=768; ATTN_DM=256; ATTN_HEADS=4; ATTN_NBLK=(1 if SMOKE else 2); ATTN_MLP=2
STEPS=40 if SMOKE else 4000; CKPT_STEPS=20 if SMOKE else 500; LR=1e-3
FT_STEPS=20 if SMOKE else 300; FT_LR=3e-4
N_TRAIN=8 if SMOKE else 96; N_HOLD2=4 if SMOKE else 16; N_SACRED=4 if SMOKE else 16
TRAIN_SEED0=7000; HOLD2_SEED0=8000
P_TRAIN=(64,384); P_WITHIN=(384,512); P_REPERA=(64,512)
# banked anchors (byte-replay before dependent bands; pre-reg block)
WALL_S4_B5=3.46003; FLOOR_B5_RECAL=0.1279
S9X_SACRED=0.11172; S9X_HOLD2=0.1317; W0_B5_BANK=1.5949
V6_R48_REP={8:0.04536,9:0.05499,10:0.07573,11:0.13158}; B12_R48_BANK=0.18155
DEC_V6_SHA="a2d384d29c27fb91"
# Arm A cells (boundary, regime); ranks; replay tolerances
ARMA_CELLS=[(7,"code"),(12,"prose")] if SMOKE else \
    [(4,"code"),(5,"code"),(6,"code"),(7,"code"),(8,"code"),(9,"code"),(10,"code"),(11,"code"),(12,"prose")]
RANKS_ARMA=[20] if SMOKE else [20,48]
S7_IS_R20={8,9,10,11,12}   # V3 built O20 only at LATE b8..b12 -> r20 replays S7 there (tol 3e-3)
TOL_S4=2e-3; TOL_R20=3e-3
# Arm B boundaries + walls (banked S7==S4)
ARMB_BOUNDS=[6] if SMOKE else [6,7]
WALL_B={6:0.84522,7:1.43786}
# Arm C1 batches
C1_NB=2 if SMOKE else 5; C1_NBLK=4 if SMOKE else 16; C1_SEED0=9000; C1_SEEDSTEP=100
SOFT_COMPUTE_S=6.0*3600; HARD_WALL_S=int(11.5*3600)

RESULT_JSON=os.path.join(DIR,"_v7_result_SMOKE.json" if SMOKE else "_v7_result.json")
BASES_PT=os.path.join(DIR,"_v7_bases_SMOKE.pt" if SMOKE else "_v7_bases.pt")
torch.manual_seed(1234)

PEN=("FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md :: 'V7 -- THE FINISH-LINE RUN (FOLD THE CODE COLUMN + "
     "THE ONSET QUESTION + DISCHARGE THE ASTERISK) -- GAP-SCAN + PRE-REGISTRATION (2026-07-05 ~22:35)'")
res={"experiment":"V7 finish-line run: Arm A folded r48 at code b4..b11 + prose_b12 (Arm-B recipe "
     "verbatim, replay-gated); Arm B onset surrogate at BUS[6]/BUS[7] (contracts CT-A/CT-B/CT-C, "
     "linear-first ladder, SACRED held-out-period falsifier); Arm C1 frozen decoder_v6 across 5 "
     "fresh held-out batches; Arm C2 front-door ablation; verdict recompute BOTH meters recal primary",
     "date":"2026-07-05","propose_only":True,"pre_registration":PEN,
     "config":{"n_train":N_TRAIN,"n_hold2":N_HOLD2,"n_sacred":N_SACRED,"steps":STEPS,"lr":LR,
        "arma_cells":[f"{r}_b{b}" for (b,r) in ARMA_CELLS],"ranks_arma":RANKS_ARMA,
        "armb_bounds":ARMB_BOUNDS,"walls_b":WALL_B,"c1_batches":C1_NB,"c1_seed0":C1_SEED0,
        "precision":"fp32","tf32":"off","attn":"eager","seed":1234,"smoke":SMOKE},
     "gpu_free_checks":[],"instrument_discrepancy":[],
     "gates":{},"c1":{},"armA":{},"c2":{},"armB":{},"verdict":{},"status":"INIT"}

def sha256(path):
    try:
        h=hashlib.sha256()
        with open(path,"rb") as f:
            for chunk in iter(lambda:f.read(1<<20),b""): h.update(chunk)
        return h.hexdigest()[:16]
    except Exception as e: return f"ERR:{e}"
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
        for k in ("gates","c1","armA","c2","armB","verdict","gpu_free_checks","instrument_discrepancy"):
            if prev.get(k): res[k]=prev[k]
        logln(f"*** RESUME *** prior elapsed={prev.get('elapsed_s')}")
    except Exception as e: logln(f"resume load fail {e}")
if os.path.exists(BASES_PT):
    try: BASES=torch.load(BASES_PT,map_location="cpu",weights_only=False); logln(f"*** RESUME bases {sorted(map(str,BASES.keys()))[:24]}")
    except Exception as e: logln(f"bases load fail {e}"); BASES={}
write_json()

# ---------------- GPU free-check (verbatim from _v5.py/_v6.py) ----------------
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
    if rec["foreign"]:
        res["instrument_discrepancy"].append({"stage":tag,"name":"gpu_free_check","why":str(rec["foreign"])})
    res["gpu_free_checks"].append(rec); write_json(); logln(f"[gpu {tag}] clear={rec['clear']}"); return rec["clear"]
def free(): gc.collect(); torch.cuda.empty_cache()

# ---------------- model (loader verbatim) ----------------
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
    M["d"]=model.config.n_embd; M["nL"]=model.config.n_layer; M["nH"]=model.config.n_head
    M["wte"]=model.transformer.wte.weight
    res["gpt2_meta"]={"n_layer":M["nL"],"d":M["d"],"n_head":M["nH"],"precision":"fp32","tf32":"off","attn":"eager"}
    logln(f"[gpt2] loaded fp32 eager nL={M['nL']} d={M['d']} nH={M['nH']}")

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
def build_dind_seeds(seed0,n):
    rows=[build_dind(1,CERT_BLOCK,seed0+i) for i in range(n)]
    return torch.cat(rows,0)
def ids_window(all_ids,lo,hi,what):
    if len(all_ids)<hi: raise RuntimeError(f"{what}: {len(all_ids)}<{hi}")
    n=(hi-lo)//CERT_BLOCK; return torch.tensor(all_ids[lo:hi],dtype=torch.long).view(n,CERT_BLOCK)

# ---------------- objects + M0a content gate (VERBATIM from _v5.py/_v6.py) ----------------
ROOMS=[2,5,3,4,6]
J1_BANKED={0:{"m_star":3.32735,"prose":0.1856,"code":0.21775,"repetition":1.20131},
 1:{"m_star":28.40602,"prose":0.18318,"code":0.2236,"repetition":0.13455},
 2:{"m_star":17.07425,"prose":0.19183,"code":0.24188,"repetition":0.16051},
 3:{"m_star":20.74943,"prose":0.18862,"code":0.22101,"repetition":0.51223},
 4:{"m_star":24.94407,"prose":0.18712,"code":0.19473,"repetition":0.41945},
 5:{"m_star":28.10003,"prose":0.18355,"code":0.19684,"repetition":0.12231},
 6:{"m_star":33.41676,"prose":0.18273,"code":0.18646,"repetition":0.07765},
 7:{"m_star":39.73945,"prose":0.19098,"code":0.19793,"repetition":0.0997},
 8:{"m_star":47.25844,"prose":0.18865,"code":0.17497,"repetition":0.08828},
 9:{"m_star":56.20007,"prose":0.18491,"code":0.15937,"repetition":0.11206},
 10:{"m_star":69.79249,"prose":0.18621,"code":0.15106,"repetition":0.11632},
 11:{"m_star":84.81515,"prose":0.18521,"code":0.1388,"repetition":0.08944},
 12:{"m_star":96.58652,"prose":0.18978,"code":0.13981,"repetition":0.07056}}
def load_objects():
    dv=torch.load(os.path.join(DIR,"decoder_v0_tensors.pt"),map_location="cpu",weights_only=False)
    C=dv["C"].float(); Qu=dv["Q_union"].float(); Qh=dv["host_Q"].float()
    hopW=dv["hop_W"].float(); hopc=dv["hop_c"].float()
    t15=torch.load(os.path.join(DIR,"_t15_bases.pt"),map_location="cpu",weights_only=False)
    t10=torch.load(os.path.join(DIR,"_t10_bases.pt"),map_location="cpu",weights_only=False)
    Qa=t10["Q_attn"].float(); Qm=t10["Q_mlp"].float()
    o1=torch.load(os.path.join(DIR,"_open1_bases.pt"),map_location="cpu",weights_only=False)
    mu=o1["mu"].float(); B2=o1["B2"].float(); U=o1["U"].float()
    o2=torch.load(os.path.join(DIR,"_open2_bases.pt"),map_location="cpu",weights_only=False)
    WF3=o2["W_F3"].float(); cF3=o2["c_F3"].float(); WF1=o2["W_F1"].float()
    v1=torch.load(os.path.join(DIR,"decoder_v1_tensors.pt"),map_location="cpu",weights_only=False)
    wte_W=v1["wte_W"].float(); wte_c=v1["wte_c"].float()
    Q35v1=v1["Q35"].float(); B2v1=v1["B2"].float(); muv1=v1["mu"].float()
    def md(a,b): return float((a.float()-b.float()).abs().max())
    cm={"C_vs_t15":md(C,t15["core_j0_5basis"]),"Qu_vs_t10":md(Qu,t10["Q_union"]),
        "WF1_vs_hopW":md(WF1,hopW),"B2_vs_v1":md(B2,B2v1),"mu_vs_v1":md(mu,muv1)}
    orthC=float((C.t()@C-torch.eye(C.shape[1])).norm())
    orthB2=float((B2.t()@B2-torch.eye(B2.shape[1])).norm())
    p4=json.load(open(os.path.join(DIR,"_open4_probe.json"),encoding="utf-8"))
    frozen=[(r["room"],r["dim"]) for r in p4["selection"]["corridor_distinct"]]
    seen=[]; kept=[]
    for b in ROOMS:
        for i in range(16):
            u=U[b][:,i]; best=0.0
            for (kb,ki,v) in seen:
                dd=abs(float(u@v))
                if dd>best: best=dd
            if best<=0.8: kept.append((b,i))
            seen.append((b,i,u))
    corr_match=bool(kept==frozen)
    V35=torch.stack([U[r][:,d_] for (r,d_) in frozen],1)
    Rr=V35-B2@(B2.t()@V35); Q35,_=torch.linalg.qr(Rr,mode='reduced')
    q35orth=float((Q35.t()@Q35-torch.eye(Q35.shape[1])).norm())
    maxB2tQ35=float((B2.t()@Q35).abs().max())
    q35_vs_v1=md(Q35,Q35v1)
    o5=json.load(open(os.path.join(DIR,"_open5_result.json"),encoding="utf-8"))
    floors={int(b):{"prose":0.1871,"code":o5["J1"]["floors"][str(b)]["code"],
                    "repetition":o5["J1"]["floors"][str(b)]["repetition"]} for b in range(13)}
    mstars={int(b):o5["J1"]["floors"][str(b)]["m_star"] for b in range(13)}
    p6=json.load(open(os.path.join(DIR,"_open6_probe.json"),encoding="utf-8"))
    floors_match=all(abs(floors[b][r]-p6["frozen"]["floors"][str(b)][r])==0.0
                     for b in range(13) for r in REGIMES)
    bank_match=all(abs(J1_BANKED[b]["m_star"]-mstars[b])==0.0 and
                   abs(J1_BANKED[b]["code"]-floors[b]["code"])==0.0 and
                   abs(J1_BANKED[b]["repetition"]-floors[b]["repetition"])==0.0 for b in range(13))
    m0a_ok=(all(v==0.0 for v in cm.values()) and orthC<=1e-4 and orthB2<=1e-3 and corr_match
            and q35orth<=1e-3 and maxB2tQ35<=1e-3 and floors_match and q35_vs_v1<=1e-5 and bank_match)
    res["gates"]["M0a"]={"content_match":cm,"core_orth":orthC,"B2_orth":orthB2,
        "corridor_recompute_match":corr_match,"Q35_orth":q35orth,"maxB2tQ35":maxB2tQ35,
        "Q35_vs_v1":q35_vs_v1,"floors_match_frozen":floors_match,"j1_bank_match":bank_match,
        "n_corridor":len(frozen),"pass":bool(m0a_ok)}
    if not m0a_ok: res["instrument_discrepancy"].append({"stage":"M0a","name":"content_or_selection","why":res["gates"]["M0a"]})
    logln(f"[M0a] cm={cm} corr_match={corr_match} floors_match={floors_match} bank={bank_match} -> {'PASS' if m0a_ok else 'FAIL'}")
    write_json()
    src_sha={f:sha256(os.path.join(DIR,f)) for f in ("decoder_v1_tensors.pt","decoder_v3_tensors.pt",
             "decoder_v6_tensors.pt","decoder_v6.json","_open1_bases.pt","_open5_result.json",
             "_v5_floors_recal.json","_v3_result.json","_v6_result.json")}
    return dict(C=C,mu=mu,B2=B2,U=U,V35=V35,Q35=Q35,frozen=frozen,floors=floors,mstars=mstars,
                wte_W=wte_W,wte_c=wte_c,src_sha=src_sha)

# ---------------- captures / KL / inject (VERBATIM) ----------------
def capture_h_all(ids_cpu,chunk,tag,which=None):
    model=M["m"]; nL=M["nL"]; N=ids_cpu.shape[0]
    which=which if which is not None else list(range(nL+1))
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
    return H
def fkl(yt,yp):
    logp=Fnn.log_softmax(yt,-1); p=logp.exp(); lp=Fnn.log_softmax(yp,-1)
    return (p*(logp-lp)).sum(-1)
class InjectHook:
    def __init__(self,block):
        self.on=False; self.add=None; self.handle=block.register_forward_hook(self._h)
    def _h(self,mod,inp,out):
        if not self.on: return None
        hs=out[0] if isinstance(out,tuple) else out; hs2=hs+self.add
        return (hs2,)+tuple(out[1:]) if isinstance(out,tuple) else hs2
    def close(self): self.handle.remove()
def clean_logits(ids_cpu):
    model=M["m"]; N=ids_cpu.shape[0]; outs=[]
    with torch.no_grad():
        for s0 in range(0,N,MB):
            s1=min(N,s0+MB); outs.append(model(ids_cpu[s0:s1].to('cuda'),use_cache=False).logits.detach())
    return outs
def inject_kl_full(ids_cpu,injhook,delta_full_g,Yclean,want_dl=False):
    model=M["m"]; N=ids_cpu.shape[0]; tot=0.0; cnt=0; ci=0; dl=0.0
    with torch.no_grad():
        for s0 in range(0,N,MB):
            s1=min(N,s0+MB)
            injhook.add=delta_full_g[s0:s1]; injhook.on=True
            lg=model(ids_cpu[s0:s1].to('cuda'),use_cache=False).logits; injhook.on=False; injhook.add=None
            if want_dl: dl=max(dl,float((lg.float()-Yclean[ci].float()).abs().max()))
            kl=fkl(Yclean[ci].float(),lg.float()); tot+=kl.sum().item(); cnt+=kl.numel(); ci+=1
            del lg
    return (tot/max(1,cnt),dl) if want_dl else tot/max(1,cnt)
def inject_kl_pidx(ids_cpu,injhook,delta_full_g,Yclean,pidx):
    model=M["m"]; N=ids_cpu.shape[0]; tot=0.0; cnt=0; ci=0
    with torch.no_grad():
        for s0 in range(0,N,MB):
            s1=min(N,s0+MB)
            injhook.add=delta_full_g[s0:s1]; injhook.on=True
            lg=model(ids_cpu[s0:s1].to('cuda'),use_cache=False).logits; injhook.on=False; injhook.add=None
            kl=fkl(Yclean[ci].float(),lg.float())[:,pidx]; tot+=kl.sum().item(); cnt+=kl.numel(); ci+=1
            del lg
    return tot/max(1,cnt)

# ---------------- surrogate rungs (VERBATIM classes, fin parameterized) ----------------
class LinearRung(nn.Module):
    def __init__(self,fin,d): super().__init__(); self.w=nn.Linear(fin,d)
    def forward(self,x): return self.w(x)
class MLPRung(nn.Module):
    def __init__(self,fin,h,d): super().__init__(); self.f1=nn.Linear(fin,h); self.act=nn.GELU(); self.f2=nn.Linear(h,d)
    def forward(self,x): return self.f2(self.act(self.f1(x)))
class AttnBlock(nn.Module):
    def __init__(self,dm,nh,mlp):
        super().__init__(); self.ln1=nn.LayerNorm(dm); self.attn=nn.MultiheadAttention(dm,nh,batch_first=True)
        self.ln2=nn.LayerNorm(dm); self.mlp=nn.Sequential(nn.Linear(dm,dm*mlp),nn.GELU(),nn.Linear(dm*mlp,dm))
    def forward(self,x,mask):
        q=self.ln1(x); a,_=self.attn(q,q,q,attn_mask=mask,need_weights=False)
        x=x+a; x=x+self.mlp(self.ln2(x)); return x
class AttnRung(nn.Module):
    def __init__(self,fin,dm,nh,nblk,mlp,d,seqlen):
        super().__init__(); self.inp=nn.Linear(fin,dm); self.pos=nn.Parameter(torch.zeros(1,seqlen,dm))
        self.blocks=nn.ModuleList([AttnBlock(dm,nh,mlp) for _ in range(nblk)]); self.out=nn.Linear(dm,d)
    def forward(self,x):
        T=x.shape[1]; h=self.inp(x)+self.pos[:,:T]
        mask=torch.triu(torch.full((T,T),float('-inf'),device=x.device),diagonal=1)
        for b in self.blocks: h=b(h,mask)
        return self.out(h)
def n_params(m): return int(sum(p.numel() for p in m.parameters()))
RUNG_SEED={"L0":11,"L1":22,"L2":33}
def make_rung(name,fin,seqlen):
    if name=="L0": return LinearRung(fin,M["d"])
    if name=="L1": return MLPRung(fin,MLP_H,M["d"])
    if name=="L2": return AttnRung(fin,ATTN_DM,ATTN_HEADS,ATTN_NBLK,ATTN_MLP,M["d"],seqlen)
    raise ValueError(name)

# ======================================================================================
# MAIN
# ======================================================================================
try:
    ensure_model()
    O=load_objects()
    if not res["gates"]["M0a"]["pass"]:
        res["status"]="STOPPED-GATE"; write_json(); raise RuntimeError("FB: M0a breach -> STOP")
    d=M["d"]; nL=M["nL"]
    B2_g=O["B2"].to('cuda'); Q35_g=O["Q35"].to('cuda'); span5=torch.cat([B2_g,Q35_g],1)
    mu_all=O["mu"]
    wteW_g=O["wte_W"].to('cuda'); wtec_g=O["wte_c"].to('cuda')
    wte_g=M["wte"].detach().float()
    def proj_compl(x): return x-(x@span5)@span5.t()
    def s4_delta(Xc,b,Ecur_all):
        b2P=(Xc@B2_g)@B2_g.t(); q35P=(Xc@Q35_g)@Q35_g.t()
        yhat=Ecur_all@wteW_g[b].t()+wtec_g[b]
        y2=yhat-(yhat@B2_g)@B2_g.t(); y4=y2-(y2@Q35_g)@Q35_g.t()
        return b2P+q35P+y4-Xc

    # frozen decoder_v6 (hash gate; C1 + CT-A depend on it)
    dv6_sha=sha256(os.path.join(DIR,"decoder_v6_tensors.pt"))
    dv6_ok=(dv6_sha==DEC_V6_SHA)
    if not dv6_ok:
        res["instrument_discrepancy"].append({"stage":"gates","name":"decoder_v6_hash","why":dv6_sha})
    dv6=torch.load(os.path.join(DIR,"decoder_v6_tensors.pt"),map_location="cpu",weights_only=False)
    v6L0=LinearRung(1537,d).to('cuda').eval()
    v6L0.load_state_dict({k:v.to('cuda') for k,v in dv6["surrogate_state_dict"].items()})
    sc6_mean=dv6["surrogate_scaler_mean"].to('cuda'); sc6_std=dv6["surrogate_scaler_std"].to('cuda')
    Vk=dv6["m0_repera_Vk_recal"].to('cuda').float()
    v5b=torch.load(os.path.join(DIR,"_v5_bases.pt"),map_location="cpu",weights_only=False)
    cos_vk=float((Vk[:,0]@v5b["m0_repera_Vk_recal"].to('cuda').float()[:,0]).abs())
    res["gates"]["decoder_v6"]={"sha":dv6_sha,"sha_ok":bool(dv6_ok),"rung":dv6.get("surrogate_rung"),
                                "vk_cos_vs_v5":round(cos_vk,6)}
    write_json(); logln(f"[gates] decoder_v6 sha={dv6_sha} ok={dv6_ok} vk_cos={cos_vk:.6f}")
    if not dv6_ok: raise RuntimeError("FB: frozen decoder_v6 hash mismatch -> STOP")

    # floors + banked V3 cells
    frec=json.load(open(os.path.join(DIR,"_v5_floors_recal.json"),encoding="utf-8"))
    floors_leg={int(b):{k:float(v) for k,v in frec["floors_legacy"][str(b)].items()} for b in range(13)}
    floors_rec={int(b):{k:(float(v) if v is not None else None) for k,v in frec["floors_recal"][str(b)].items()} for b in range(13)}
    RECAL_OK=(not frec.get("quarantined")) and frec.get("sg_early_ok") and frec.get("repl_all")
    v3=json.load(open(os.path.join(DIR,"_v3_result.json"),encoding="utf-8"))
    v3cells=v3["cells"]
    logln(f"[floors] RECAL_OK={RECAL_OK} rep_b6={floors_rec[6]['repetition']} rep_b7={floors_rec[7]['repetition']}")

    WIKI=M["tok"](load_wiki_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
    CIDS=M["tok"](load_code_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
    IDS_SACRED=build_dind(N_SACRED,CERT_BLOCK,REP_SEED)
    IDS_TRAIN=build_dind_seeds(TRAIN_SEED0,N_TRAIN)
    IDS_HOLD2=build_dind_seeds(HOLD2_SEED0,N_HOLD2)

    # ---------------- feature builders (b5 contract verbatim; b6/b7 contracts per pre-reg) ----------
    CAPB=[2,5,6,7]   # boundaries captured for feature/object building
    CAPS={}          # in-memory capture cache (deterministic; recaptured on resume, NOT persisted)
    CAP_IDS={"train":IDS_TRAIN,"sacred":IDS_SACRED,"hold2":IDS_HOLD2}
    def get_cap(name):
        if name not in CAPS: CAPS[name]=capture_feats_multi(CAP_IDS[name],name)
        return CAPS[name]
    def capture_feats_multi(ids_cpu,tag):
        model=M["m"]; N=ids_cpu.shape[0]; buf={}
        def mkh(key,idx):
            def h(mod,inp,out): buf[key]=(out[0] if isinstance(out,tuple) else out).detach()
            return h
        hh=[M['blocks'][bb-1].register_forward_hook(mkh(f'h{bb}',bb)) for bb in CAPB]
        hh.append(M['blocks'][0].mlp.register_forward_hook(
            lambda m,i,o: buf.__setitem__('wm0',o.detach())))
        acc={f'h{bb}':[] for bb in CAPB}; acc['wm0']=[]
        with torch.no_grad():
            for c0 in range(0,N,CAP_CHUNK):
                c1=min(N,c0+CAP_CHUNK); _=model(ids_cpu[c0:c1].to('cuda'),use_cache=False)
                for k in acc: acc[k].append(buf[k].reshape(-1,d).cpu())
        for x in hh: x.remove()
        logln(f"[feats {tag}] N={N} captured {list(acc.keys())}")
        return {k:torch.cat(v) for k,v in acc.items()}
    def base_feats(cap,ids_cpu):
        # returns x2, ecur, s (GPU) from a capture dict
        x2=cap['h2'].to('cuda')-mu_all[B2b].to('cuda')
        ecur=wte_g[ids_cpu.reshape(-1).to('cuda')]
        s=cap['wm0'].to('cuda')@Vk
        return x2,ecur,s
    def obj_at(cap,b):
        return proj_compl(cap[f'h{b}'].to('cuda')-mu_all[b].to('cuda'))
    def obj5hat_of(x2,ecur,s):
        f6=torch.cat([x2,ecur,s],1)
        with torch.no_grad():
            oh=proj_compl(v6L0((f6-sc6_mean)/sc6_std))
        return oh
    def contract_feats(ct,cap,ids_cpu,extra=None):
        x2,ecur,s=base_feats(cap,ids_cpu)
        if ct=="CTB": return torch.cat([x2,ecur,s],1)
        if ct=="CTA": return torch.cat([x2,ecur,s,obj5hat_of(x2,ecur,s)],1)
        if ct=="C2":  return torch.cat([x2,ecur],1)
        if ct=="CTC":
            o5=obj5hat_of(x2,ecur,s)
            return torch.cat([x2,ecur,s,o5,extra],1)   # extra = obj6hat (GPU, Ntok x d)
        raise ValueError(ct)
    CT_FIN={"CTB":1537,"CTA":2305,"C2":1536,"CTC":3073}

    def substitution_kl_at(b,oh,obj_g,ids_cpu,Ycl,injhook,want_behav=False):
        N=ids_cpu.shape[0]
        delta=(oh-obj_g).reshape(N,CERT_BLOCK,d).clone(); delta[:, :IND_SEG, :]=0.0
        pidx_rep=torch.arange(IND_SEG,CERT_BLOCK)
        kl_rep=inject_kl_pidx(ids_cpu,injhook,delta,Ycl,pidx_rep)
        kl_all,dl=inject_kl_full(ids_cpu,injhook,delta,Ycl,want_dl=True)
        out={"kl_rep":round(kl_rep,5),"kl_all":round(kl_all,5),"max_dlogit":round(dl,5)}
        if want_behav: out["behav"]=behav_meter(oh,obj_g,ids_cpu,Ycl,injhook)
        return out
    def behav_meter(oh,obj_g,ids_cpu,Ycl,injhook):
        N=ids_cpu.shape[0]
        delta=(oh-obj_g).reshape(N,CERT_BLOCK,d).clone(); delta[:, :IND_SEG, :]=0.0
        pc=0.0;ps=0.0;ac=0.0;as_=0.0;cnt=0;ci=0
        with torch.no_grad():
            for s0 in range(0,N,MB):
                s1=min(N,s0+MB)
                injhook.add=delta[s0:s1]; injhook.on=True
                lg=M["m"](ids_cpu[s0:s1].to('cuda'),use_cache=False).logits.float(); injhook.on=False; injhook.add=None
                yc=Ycl[ci].float()
                nxt=ids_cpu[s0:s1,IND_SEG+1:CERT_BLOCK].to('cuda')
                lc=yc[:,IND_SEG:CERT_BLOCK-1]; lsb=lg[:,IND_SEG:CERT_BLOCK-1]
                pcl=Fnn.softmax(lc,-1).gather(-1,nxt[...,None]).squeeze(-1)
                psb=Fnn.softmax(lsb,-1).gather(-1,nxt[...,None]).squeeze(-1)
                pc+=float(pcl.sum()); ps+=float(psb.sum())
                ac+=float((lc.argmax(-1)==nxt).sum()); as_+=float((lsb.argmax(-1)==nxt).sum())
                cnt+=nxt.numel(); ci+=1; del lg
        pc/=cnt; ps/=cnt; ac/=cnt; as_/=cnt
        return {"p_true_clean":round(pc,5),"p_true_sub":round(ps,5),"copy_fidelity_ratio":round(ps/max(pc,1e-9),4),
                "argmax_copy_clean":round(ac,4),"argmax_copy_sub":round(as_,4),"n":cnt}
    def r2_of(oh,obj_g,N):
        m=torch.zeros(N,CERT_BLOCK,dtype=torch.bool); m[:,IND_SEG:CERT_BLOCK]=True; m=m.reshape(-1).to('cuda')
        e=((oh[m]-obj_g[m])**2).sum(); v=((obj_g[m]-obj_g[m].mean(0))**2).sum()
        return float(1-(e/v.clamp(min=1e-9)))

    # =================================================================================
    # STAGE G -- global b5 instrument gates (identity / S4 byte-replay / SILENT) on SACRED
    # =================================================================================
    if not res["gates"].get("b5"):
        gpu_free_check("gates-b5")
        logln("==== GATES: b5 identity / S4 replay / SILENT on SACRED ====")
        cap_s=get_cap("sacred")
        Xc5=cap_s['h5'].to('cuda')-mu_all[B5].to('cuda'); obj_s5=proj_compl(Xc5)
        N=IDS_SACRED.shape[0]; Ycl_s=clean_logits(IDS_SACRED)
        inj5=InjectHook(M["blocks"][B5-1])
        zero=torch.zeros(N,CERT_BLOCK,d,device='cuda')
        kl_id,dl_id=inject_kl_full(IDS_SACRED,inj5,zero,Ycl_s,want_dl=True)
        Ecur=wte_g[IDS_SACRED.reshape(-1).to('cuda')]
        kl_S4=inject_kl_full(IDS_SACRED,inj5,s4_delta(Xc5,B5,Ecur).reshape(N,CERT_BLOCK,d),Ycl_s)
        dsil=(-obj_s5).reshape(N,CERT_BLOCK,d).clone(); dsil[:, :IND_SEG, :]=0.0
        kl_sil_rep=inject_kl_pidx(IDS_SACRED,inj5,dsil,Ycl_s,torch.arange(IND_SEG,CERT_BLOCK))
        s4_ok=(abs(kl_S4-WALL_S4_B5)<=TOL_S4 and kl_id==0.0 and dl_id==0.0) if not SMOKE else (kl_id==0.0)
        if not s4_ok: res["instrument_discrepancy"].append({"stage":"gates-b5","name":"S4/identity","why":{"S4":kl_S4,"id":kl_id,"dl":dl_id}})
        # S9x replay: frozen v6 L0 on SACRED must reproduce the banked cert number to the digit
        x2,ecur,s=base_feats(cap_s,IDS_SACRED)
        oh5=obj5hat_of(x2,ecur,s)
        sub=substitution_kl_at(B5,oh5,obj_s5,IDS_SACRED,Ycl_s,inj5)
        s9x_ok=(abs(sub["kl_rep"]-S9X_SACRED)<=TOL_S4) if not SMOKE else True
        if not s9x_ok: res["instrument_discrepancy"].append({"stage":"gates-b5","name":"S9x_replay","why":sub})
        inj5.close()
        res["gates"]["b5"]={"identity_kl":kl_id,"identity_dlogit":dl_id,"S4_replay":round(kl_S4,5),
            "S4_banked":WALL_S4_B5,"S4_ok":bool(s4_ok),"silent_rep":round(kl_sil_rep,5),
            "S9x_replay":sub["kl_rep"],"S9x_banked":S9X_SACRED,"S9x_ok":bool(s9x_ok)}
        write_json()
        logln(f"[gates-b5] id={kl_id}/{dl_id} S4={kl_S4:.5f}(bk {WALL_S4_B5}) sil={kl_sil_rep:.5f} "
              f"S9x={sub['kl_rep']:.5f}(bk {S9X_SACRED}) -> {'OK' if (s4_ok and s9x_ok) else 'FAIL'}")
        del Xc5,obj_s5,Ycl_s,zero,Ecur,x2,ecur,s,oh5; free()

    # =================================================================================
    # ARM C1 -- discharge the asterisk: frozen v6 L0 across fresh held-out batches
    # =================================================================================
    if not res["c1"].get("done") and el()<HARD_WALL_S:
        gpu_free_check("c1")
        logln("==== ARM C1: frozen decoder_v6 across fresh held-out batches ====")
        rows=res["c1"].get("rows",{})
        inj5=InjectHook(M["blocks"][B5-1])
        for j in range(C1_NB):
            key=f"batch{j}"
            if rows.get(key,{}).get("done"): continue
            seed0=C1_SEED0+C1_SEEDSTEP*j
            ids=build_dind_seeds(seed0,C1_NBLK)
            cap=capture_feats_multi(ids,f"c1-{j}")
            x2,ecur,s=base_feats(cap,ids)
            oh=obj5hat_of(x2,ecur,s); obj=obj_at(cap,B5)
            Ycl=clean_logits(ids)
            kl_id,_=inject_kl_full(ids,inj5,torch.zeros(ids.shape[0],CERT_BLOCK,d,device='cuda'),Ycl,want_dl=True)
            sub=substitution_kl_at(B5,oh,obj,ids,Ycl,inj5)
            rows[key]={"done":True,"seed0":seed0,"n_blocks":int(ids.shape[0]),"identity_kl":kl_id,
                       "kl_rep":sub["kl_rep"],"kl_all":sub["kl_all"],"r2":round(r2_of(oh,obj,ids.shape[0]),4)}
            res["c1"]["rows"]=rows; write_json()
            logln(f"[c1 {key}] seed0={seed0} kl_rep={sub['kl_rep']:.5f} r2={rows[key]['r2']}")
            del cap,x2,ecur,s,oh,obj,Ycl; free()
        inj5.close()
        vals=sorted(rows[f"batch{j}"]["kl_rep"] for j in range(C1_NB) if rows.get(f"batch{j}",{}).get("done"))
        if len(vals)==C1_NB:
            med=vals[len(vals)//2] if len(vals)%2==1 else 0.5*(vals[len(vals)//2-1]+vals[len(vals)//2])
            mx=max(vals)
            if med<=FLOOR_B5_RECAL and mx<=2*FLOOR_B5_RECAL: band="DISCHARGED"
            elif med<=S9X_HOLD2 and mx<=2*FLOOR_B5_RECAL: band="HOLDS-THIN"
            else: band="FAILS"
            res["c1"].update({"done":True,"values":vals,"median":round(med,5),"max":round(mx,5),
                "floor":FLOOR_B5_RECAL,"H_V7_C1":band,
                "bands":"DISCHARGED med<=0.1279 & max<=0.2558 / HOLDS-THIN med<=0.1317 & max<=0.2558 / FAILS",
                "bet":"DISCHARGED 55 / HOLDS-THIN 30 / FAILS 15"})
            write_json(); logln(f"[C1] values={vals} median={med:.5f} max={mx:.5f} -> H-V7-C1={band}")

    # =================================================================================
    # ARM A -- folded r20/r48 at code b4..b11 + prose_b12 (Arm-B recipe VERBATIM)
    # =================================================================================
    if not res["armA"].get("done") and el()<HARD_WALL_S:
        gpu_free_check("armA")
        logln("==== ARM A: folded r-cap reads, code column + prose_b12 ====")
        STREAMS_A={"prose":ids_window(WIKI,FRESH_LO,FRESH_HI,"fresh prose")[:N_SACRED],
                   "repetition":IDS_SACRED}
        try: STREAMS_A["code"]=ids_window(CIDS,FRESH_LO,FRESH_HI,"fresh code")[:N_SACRED]
        except Exception as e: logln(f"[armA] code load failed {e}")
        bounds_needed=sorted({b for (b,_) in ARMA_CELLS})
        if not SMOKE and len(STREAMS_A)!=3:
            res["instrument_discrepancy"].append({"stage":"armA","name":"stream_count","why":list(STREAMS_A)})
        # one capture pass per stream for all needed boundaries (deterministic; CAP_CHUNK verbatim;
        # in-memory only -- recaptured on resume, ~1 min)
        caps={}
        for reg in REGIMES:
            if reg not in STREAMS_A: continue
            caps[reg]=capture_h_all(STREAMS_A[reg],CAP_CHUNK,f"armA-{reg}",which=bounds_needed)
        Ycl_cache={}
        arma=res["armA"].get("cells",{})
        for (b,reg) in ARMA_CELLS:
            key=f"{reg}_b{b}"
            if arma.get(key,{}).get("done"): continue
            if el()>HARD_WALL_S: break
            gram=torch.zeros(d,d,dtype=torch.float64); ntok=0
            B2d=B2_g.double()
            for reg2 in REGIMES:
                if reg2 not in caps: continue
                h=caps[reg2][b].to('cuda').double(); rr=h-mu_all[b].to('cuda').double(); rr=rr-(rr@B2d)@B2d.t()
                gram+=(rr.t()@rr).cpu().double(); ntok+=rr.shape[0]; del h,rr; free()
            G=gram/max(1,ntok); evals,evecs=torch.linalg.eigh(G); evals=evals.clamp(min=0)
            order=torch.argsort(evals,descending=True); V=evecs[:,order].float().to('cuda')
            ids_t=STREAMS_A[reg]; NHt=ids_t.shape[0]
            if reg not in Ycl_cache: Ycl_cache[reg]=clean_logits(ids_t)
            Yct=Ycl_cache[reg]
            Xc=caps[reg][b].to('cuda')-mu_all[b].to('cuda')
            Ecur_all=wte_g[ids_t.reshape(-1).to('cuda')]
            inj=InjectHook(M["blocks"][b-1])
            kl_idb=inject_kl_full(ids_t,inj,torch.zeros(NHt,CERT_BLOCK,d,device='cuda'),Yct)
            b2P=(Xc@B2_g)@B2_g.t(); q35P=(Xc@Q35_g)@Q35_g.t()
            yhat=Ecur_all@wteW_g[b].t()+wtec_g[b]; y2=yhat-(yhat@B2_g)@B2_g.t(); y4=y2-(y2@Q35_g)@Q35_g.t()
            # S4/wte replay leg (bank exists at every cell; at b4..b7 this IS the S7 bank)
            kl_s4c=inject_kl_full(ids_t,inj,(b2P+q35P+y4-Xc).reshape(NHt,CERT_BLOCK,d),Yct)
            bank_s4=v3cells[key]["KL"]["S4"]; bank_s7=v3cells[key]["KL"]["S7"]
            s4_ok=(abs(kl_s4c-bank_s4)<=TOL_S4) if not SMOKE else True
            replay_fail=[]
            if not s4_ok: replay_fail.append({"leg":"S4","kl":kl_s4c,"banked":bank_s4})
            curve={}
            for rk in RANKS_ARMA:
                Ok=V[:, :rk]; Op=Ok-span5@(span5.t()@Ok)
                Usvd,Ssvd,_=torch.linalg.svd(Op,full_matrices=False); keep=Ssvd>1e-2; O_r=Usvd[:,keep].contiguous()
                net=int(O_r.shape[1])
                oP=(Xc@O_r)@O_r.t(); yk=y4-(y4@O_r)@O_r.t()
                kl=inject_kl_full(ids_t,inj,(b2P+q35P+oP+yk-Xc).reshape(NHt,CERT_BLOCK,d),Yct)
                ok=True
                if rk==20 and b in S7_IS_R20 and not SMOKE:
                    ok=(abs(kl-bank_s7)<=TOL_R20)
                    if not ok: replay_fail.append({"leg":"r20","kl":kl,"banked":bank_s7})
                curve[str(rk)]={"net_dims":net,"KL":round(kl,5),"replay_ok":bool(ok),"total_unnamed_folded":14+net}
                if rk==48: BASES[f"O_r48_{key}"]=O_r.cpu().contiguous(); save_bases()
                logln(f"[armA {key} r{rk}] net={net} KL={kl:.5f} (S7 bank {bank_s7}) ok={ok}")
            inj.close()
            if replay_fail: res["instrument_discrepancy"].append({"stage":"armA-replay","name":key,"why":replay_fail})
            kl48=curve.get("48",{}).get("KL")
            fl_rec=floors_rec[b][reg] if reg!="prose" else 0.1871
            fl_leg=floors_leg[b][reg]
            gates_ok=bool(kl_idb==0.0 and s4_ok and not replay_fail)
            closes=bool(kl48 is not None and fl_rec is not None and kl48<=fl_rec and gates_ok and RECAL_OK)
            arma[key]={"done":True,"identity_kl":kl_idb,"S4_replay":round(kl_s4c,5),"S4_banked":bank_s4,
                "S7_banked":bank_s7,"curve":curve,"KL_r48":kl48,"gates_ok":gates_ok,
                "floor_recal":fl_rec,"floor_legacy":fl_leg,
                "H_V7_A":("CLOSES-RECAL" if closes else "STAYS"),
                "legacy_leg":{"KL":kl48,"floor":fl_leg,"pass":bool(kl48 is not None and kl48<=fl_leg)}}
            res["armA"]["cells"]=arma; write_json()
            logln(f"[armA {key}] r48={kl48} vs recal {fl_rec} legacy {fl_leg} -> {arma[key]['H_V7_A']}")
            del V,G,evecs,evals,Xc,Ecur_all,b2P,q35P,yhat,y2,y4; free()
        res["armA"]["done"]=True; write_json()
        del Ycl_cache; free()

    # =================================================================================
    # shared: TRAIN capture (for C2 + Arm B) + eval captures
    # =================================================================================
    need_train=(not res["c2"].get("done")) or (not res["armB"].get("done"))
    if need_train and el()<HARD_WALL_S:
        gpu_free_check("capture-train")
        cap_tr=get_cap("train"); cap_sac=get_cap("sacred"); cap_h2=get_cap("hold2")
        Ntr=IDS_TRAIN.shape[0]
        maskrows=torch.zeros(Ntr,CERT_BLOCK,dtype=torch.bool); maskrows[:,P_TRAIN[0]:P_TRAIN[1]]=True
        mrow=maskrows.reshape(-1); mrow_g=mrow.to('cuda'); mask_blk=maskrows.to('cuda')
        mwith=torch.zeros(Ntr,CERT_BLOCK,dtype=torch.bool); mwith[:,P_WITHIN[0]:P_WITHIN[1]]=True
        mwith_g=mwith.reshape(-1).to('cuda')
        BCHUNK=8 if SMOKE else 32

        def make_scaler(feats_g,tag):
            skey=f"scaler_{tag}"
            if skey in BASES:
                return BASES[skey]["mean"].to('cuda'),BASES[skey]["std"].to('cuda')
            tr_rep=feats_g[mrow_g]
            m_=tr_rep.mean(0,keepdim=True); s_=tr_rep.std(0,keepdim=True).clamp(min=1e-6)
            BASES[skey]={"mean":m_.cpu(),"std":s_.cpu()}; save_bases()
            return m_,s_

        def train_rung_v7(name,fin,feats_tr_g,obj_tr_g,seed,shuffle,tag):
            torch.manual_seed(seed)
            model=make_rung(name,fin,CERT_BLOCK).to('cuda').train()
            opt=torch.optim.Adam(model.parameters(),lr=LR)
            losses=[]
            feats_rep=feats_tr_g[mrow_g]; obj_rep=obj_tr_g[mrow_g]
            if name=="L2":
                tgt=obj_tr_g.reshape(Ntr,CERT_BLOCK,d)
                if shuffle:
                    idx=torch.randperm(int(mrow.sum()),device='cuda')
                    permd=obj_rep[idx]
                    tgt=tgt.clone(); tgt.reshape(-1,d)[mrow_g]=permd
                n_elem=float(mask_blk.sum().item()*d)
                fblk=feats_tr_g.reshape(Ntr,CERT_BLOCK,fin)
            else:
                tgt=obj_rep
                if shuffle:
                    idx=torch.randperm(tgt.shape[0],device='cuda'); tgt=tgt[idx]
            for step in range(STEPS):
                opt.zero_grad(set_to_none=True)
                if name=="L2":
                    acc=0.0
                    for c0 in range(0,Ntr,BCHUNK):
                        c1=min(Ntr,c0+BCHUNK)
                        raw=model(fblk[c0:c1])
                        oh=proj_compl(raw.reshape(-1,d)).reshape(c1-c0,CERT_BLOCK,d)
                        err=(oh-tgt[c0:c1])[mask_blk[c0:c1]]
                        loss=(err*err).sum()/n_elem
                        loss.backward(); acc+=float(loss.item())
                    losses.append(acc)
                else:
                    raw=model(feats_rep)
                    oh=proj_compl(raw)
                    err=oh-tgt; loss=(err*err).mean()
                    loss.backward(); losses.append(float(loss.item()))
                opt.step()
                if (step+1)%CKPT_STEPS==0 or step==STEPS-1:
                    BASES[f"sd_{tag}"]={k:v.detach().cpu() for k,v in model.state_dict().items()}
                    BASES[f"step_{tag}"]=step+1; save_bases()
                    logln(f"[train {tag}] step {step+1}/{STEPS} loss={losses[-1]:.5f}")
            return model.eval(),losses

        def rung_predict(model,name,fin,feats_g,N):
            with torch.no_grad():
                if name=="L2": raw=model(feats_g.reshape(N,CERT_BLOCK,fin)).reshape(-1,d)
                else: raw=model(feats_g)
                return proj_compl(raw)

        YCL={"sacred":None,"hold2":None}
        def ycl(setname,ids_cpu):
            # train logits are NEVER cached (24 x 411MB = ~10GB GPU); recomputed per use like _v6.py
            if setname=="train": return clean_logits(ids_cpu)
            if YCL[setname] is None: YCL[setname]=clean_logits(ids_cpu)
            return YCL[setname]

        # full falsifier battery for one trained rung at boundary b (SACRED primary + HOLD2 + WITHIN + twin)
        def certify_rung(b,name,ct,mr,mt,feats_by_set,obj_by_set,injb,fl_rec,tag):
            fin=CT_FIN[ct]
            oh_s=rung_predict(mr,name,fin,feats_by_set["sacred"],N_SACRED)
            sub_s=substitution_kl_at(b,oh_s,obj_by_set["sacred"],IDS_SACRED,ycl("sacred",IDS_SACRED),injb,want_behav=True)
            r2_s=r2_of(oh_s,obj_by_set["sacred"],N_SACRED)
            oh_h=rung_predict(mr,name,fin,feats_by_set["hold2"],N_HOLD2)
            sub_h=substitution_kl_at(b,oh_h,obj_by_set["hold2"],IDS_HOLD2,ycl("hold2",IDS_HOLD2),injb)
            r2_h=r2_of(oh_h,obj_by_set["hold2"],N_HOLD2)
            # WITHIN: substitute only [384,512) on train blocks
            oh_t=rung_predict(mr,name,fin,feats_by_set["train"],Ntr)
            dW=(oh_t-obj_by_set["train"]).reshape(Ntr,CERT_BLOCK,d).clone(); dW[:, :P_WITHIN[0], :]=0.0
            kl_within=inject_kl_pidx(IDS_TRAIN,injb,dW,ycl("train",IDS_TRAIN),torch.arange(P_WITHIN[0],CERT_BLOCK))
            del dW,oh_t; free()
            # twin on SACRED
            oh_tw=rung_predict(mt,name,fin,feats_by_set["sacred"],N_SACRED)
            sub_tw=substitution_kl_at(b,oh_tw,obj_by_set["sacred"],IDS_SACRED,ycl("sacred",IDS_SACRED),injb)
            r2_tw=r2_of(oh_tw,obj_by_set["sacred"],N_SACRED)
            real_kl=sub_s["kl_rep"]; twin_kl=sub_tw["kl_rep"]
            beats=bool(real_kl<=0.5*twin_kl); cert=bool(real_kl<=fl_rec and beats)
            return {"rung":name,"contract":ct,"params":n_params(mr),
                "SACRED_kl_rep":real_kl,"SACRED_kl_all":sub_s["kl_all"],"SACRED_r2":round(r2_s,4),
                "SACRED_behav":sub_s.get("behav"),
                "HOLD2_kl_rep":sub_h["kl_rep"],"HOLD2_r2":round(r2_h,4),
                "WITHIN_kl_rep":round(kl_within,5),"twin_kl_rep":twin_kl,"twin_r2":round(r2_tw,4),
                "beats_twin_2x":beats,"certified":cert,"floor":fl_rec}

        # =============================================================================
        # ARM C2 -- front-door ablation at b5: retrain L0 on [x2,ecur]
        # =============================================================================
        if not res["c2"].get("done") and el()<HARD_WALL_S:
            gpu_free_check("c2")
            logln("==== ARM C2: front-door ablation (drop m0 k*=1 coeff) at b5 ====")
            ct="C2"; fin=CT_FIN[ct]
            f_tr=contract_feats(ct,cap_tr,IDS_TRAIN)
            scm,scs=make_scaler(f_tr,"c2_b5")
            f_tr=(f_tr-scm)/scs
            obj_tr5=obj_at(cap_tr,B5)
            seed=20260707+10000*B5+1000*3+RUNG_SEED["L0"]
            if res["c2"].get("trained") and f"sd_c2_L0_real" in BASES:
                mr=make_rung("L0",fin,CERT_BLOCK).to('cuda').eval(); mr.load_state_dict({k:v.to('cuda') for k,v in BASES["sd_c2_L0_real"].items()})
                mt=make_rung("L0",fin,CERT_BLOCK).to('cuda').eval(); mt.load_state_dict({k:v.to('cuda') for k,v in BASES["sd_c2_L0_twin"].items()})
                tr_curves=res["c2"].get("curves",{})
            else:
                mr,lr_=train_rung_v7("L0",fin,f_tr,obj_tr5,seed,False,"c2_L0_real")
                mt,lt_=train_rung_v7("L0",fin,f_tr,obj_tr5,seed+1,True,"c2_L0_twin")
                tr_curves={"final_loss_real":round(lr_[-1],6),"final_loss_twin":round(lt_[-1],6)}
                res["c2"]["trained"]=True; res["c2"]["curves"]=tr_curves; write_json()
            f_sac=(contract_feats(ct,cap_sac,IDS_SACRED)-scm)/scs
            f_h2=(contract_feats(ct,cap_h2,IDS_HOLD2)-scm)/scs
            feats_by_set={"train":f_tr,"sacred":f_sac,"hold2":f_h2}
            obj_by_set={"train":obj_tr5,"sacred":obj_at(cap_sac,B5),"hold2":obj_at(cap_h2,B5)}
            injb=InjectHook(M["blocks"][B5-1])
            rec=certify_rung(B5,"L0",ct,mr,mt,feats_by_set,obj_by_set,injb,FLOOR_B5_RECAL,"c2")
            injb.close()
            kl=rec["SACRED_kl_rep"]
            if kl<=FLOOR_B5_RECAL: band="FRONT-DOOR-NOT-NEEDED"
            elif kl<=0.9*W0_B5_BANK: band="FRONT-DOOR-HELPS"
            else: band="FRONT-DOOR-ESSENTIAL"
            res["c2"].update({"done":True,"rec":rec,"H_V7_C2":band,"delta_vs_full_contract":round(kl-S9X_SACRED,5),
                "bands":"NOT-NEEDED <=0.1279 / HELPS <=1.43541 (0.9*W0 1.5949) / ESSENTIAL else",
                "bet":"HELPS 50 / NOT-NEEDED 30 / ESSENTIAL 20"})
            write_json(); logln(f"[C2] SACRED kl_rep={kl:.5f} (full-contract bank {S9X_SACRED}) -> {band}")
            del f_tr,f_sac,f_h2,obj_tr5,mr,mt,feats_by_set,obj_by_set; free()

        # =============================================================================
        # ARM B -- onset surrogate at BUS[6] / BUS[7] (linear first and favored)
        # =============================================================================
        if not res["armB"].get("done") and el()<HARD_WALL_S:
            armb=res["armB"].get("bounds",{})
            b6_cert_rung=None   # (name, ct) if b6 certified at L0 -> arms CT-C at b7
            for b in ARMB_BOUNDS:
                brec=armb.get(str(b),{})
                if brec.get("done"):
                    if b==6 and brec.get("H_V7_B","").startswith("CERTIFIES") and (brec.get("best") or {}).get("rung")=="L0":
                        b6_cert_rung=(brec["best"]["rung"],brec["best"]["contract"])
                    continue
                if el()>HARD_WALL_S: break
                gpu_free_check(f"armB-b{b}")
                logln(f"==== ARM B: onset surrogate at BUS[{b}] ====")
                fl_rec=floors_rec[b]["repetition"]; fl_leg=floors_leg[b]["repetition"]; wall=WALL_B[b]
                injb=InjectHook(M["blocks"][b-1])
                # per-boundary gates: identity / s4 replay / silent
                if not brec.get("gates"):
                    obj_s=obj_at(cap_sac,b); Nc=N_SACRED
                    Ys=ycl("sacred",IDS_SACRED)
                    kl_id,dl_id=inject_kl_full(IDS_SACRED,injb,torch.zeros(Nc,CERT_BLOCK,d,device='cuda'),Ys,want_dl=True)
                    Xcb=cap_sac[f'h{b}'].to('cuda')-mu_all[b].to('cuda')
                    Ecur=wte_g[IDS_SACRED.reshape(-1).to('cuda')]
                    kl_s4b=inject_kl_full(IDS_SACRED,injb,s4_delta(Xcb,b,Ecur).reshape(Nc,CERT_BLOCK,d),Ys)
                    dsil=(-obj_s).reshape(Nc,CERT_BLOCK,d).clone(); dsil[:, :IND_SEG, :]=0.0
                    kl_sil=inject_kl_pidx(IDS_SACRED,injb,dsil,Ys,torch.arange(IND_SEG,CERT_BLOCK))
                    s4ok=(abs(kl_s4b-wall)<=TOL_S4 and kl_id==0.0 and dl_id==0.0) if not SMOKE else (kl_id==0.0)
                    if not s4ok: res["instrument_discrepancy"].append({"stage":f"armB-b{b}","name":"S4/identity","why":{"S4":kl_s4b,"id":kl_id}})
                    brec["gates"]={"identity_kl":kl_id,"identity_dlogit":dl_id,"S4_replay":round(kl_s4b,5),
                                   "S4_banked":wall,"S4_ok":bool(s4ok),"silent_rep":round(kl_sil,5)}
                    armb[str(b)]=brec; res["armB"]["bounds"]=armb; write_json()
                    logln(f"[armB b{b} gates] id={kl_id}/{dl_id} S4={kl_s4b:.5f}(bk {wall}) sil={kl_sil:.5f} ok={s4ok}")
                    del obj_s,Xcb,Ecur,dsil; free()
                W0b=brec["gates"]["silent_rep"]
                obj_by_set={"train":obj_at(cap_tr,b),"sacred":obj_at(cap_sac,b),"hold2":obj_at(cap_h2,b)}
                attempts=brec.get("attempts",{})
                def feats_sets(ct,extra_by_set=None):
                    f_tr=contract_feats(ct,cap_tr,IDS_TRAIN,(extra_by_set or {}).get("train"))
                    scm,scs=make_scaler(f_tr,f"{ct}_b{b}")
                    return {"train":(f_tr-scm)/scs,
                            "sacred":(contract_feats(ct,cap_sac,IDS_SACRED,(extra_by_set or {}).get("sacred"))-scm)/scs,
                            "hold2":(contract_feats(ct,cap_h2,IDS_HOLD2,(extra_by_set or {}).get("hold2"))-scm)/scs}
                def run_attempt(name,ct,extra_by_set=None):
                    akey=f"{name}_{ct}"
                    if attempts.get(akey,{}).get("done"): return attempts[akey]
                    fin=CT_FIN[ct]
                    fb=feats_sets(ct,extra_by_set)
                    seedbase=20260707+10000*b+1000*{"CTA":0,"CTB":1,"CTC":2}[ct]+RUNG_SEED[name]
                    tag=f"b{b}_{akey}"
                    if f"sd_{tag}_real" in BASES and attempts.get(akey,{}).get("trained"):
                        mr=make_rung(name,fin,CERT_BLOCK).to('cuda').eval(); mr.load_state_dict({k:v.to('cuda') for k,v in BASES[f"sd_{tag}_real"].items()})
                        mt=make_rung(name,fin,CERT_BLOCK).to('cuda').eval(); mt.load_state_dict({k:v.to('cuda') for k,v in BASES[f"sd_{tag}_twin"].items()})
                        curves=attempts[akey].get("curves",{})
                    else:
                        mr,lr_=train_rung_v7(name,fin,fb["train"],obj_by_set["train"],seedbase,False,f"{tag}_real")
                        mt,lt_=train_rung_v7(name,fin,fb["train"],obj_by_set["train"],seedbase+1,True,f"{tag}_twin")
                        curves={"final_loss_real":round(lr_[-1],6),"final_loss_twin":round(lt_[-1],6)}
                        attempts[akey]={"trained":True,"curves":curves}; brec["attempts"]=attempts
                        armb[str(b)]=brec; res["armB"]["bounds"]=armb; write_json()
                    # train/within R2
                    with torch.no_grad():
                        ohtr=rung_predict(mr,name,fin,fb["train"],Ntr)
                        def r2m(mask):
                            e=((ohtr[mask]-obj_by_set["train"][mask])**2).sum()
                            v=((obj_by_set["train"][mask]-obj_by_set["train"][mask].mean(0))**2).sum()
                            return float(1-(e/v.clamp(min=1e-9)))
                        r2tr=r2m(mrow_g); r2wi=r2m(mwith_g)
                        del ohtr; free()
                    rec=certify_rung(b,name,ct,mr,mt,fb,obj_by_set,injb,fl_rec,tag)
                    rec.update({"done":True,"curves":curves,"r2_train":round(r2tr,4),"r2_within":round(r2wi,4),
                                "legacy_pass":bool(rec["SACRED_kl_rep"]<=fl_leg)})
                    attempts[akey]=rec; brec["attempts"]=attempts
                    armb[str(b)]=brec; res["armB"]["bounds"]=armb; write_json()
                    logln(f"[armB b{b} {akey}] SACRED={rec['SACRED_kl_rep']:.5f} (fl {fl_rec}, twin {rec['twin_kl_rep']:.5f}, "
                          f"W0 {W0b}) r2={rec['SACRED_r2']} hold2={rec['HOLD2_kl_rep']:.5f} within={rec['WITHIN_kl_rep']:.5f} cert={rec['certified']}")
                    del mr,mt,fb; free()
                    return attempts[akey]
                # ladder: L0 CT-A + L0 CT-B first (linear favored)
                a1=run_attempt("L0","CTA"); a2=run_attempt("L0","CTB")
                cert_recs=[r for r in (a2,a1) if r.get("certified")]   # CT-B first = minimal contract holds cert
                ladder_note="L0-only (linear favored)"
                if not cert_recs and not SMOKE and el()<HARD_WALL_S:
                    a3=run_attempt("L1","CTA"); ladder_note="L0 failed -> L1"
                    if a3.get("certified"): cert_recs=[a3]
                    elif el()<HARD_WALL_S:
                        a4=run_attempt("L2","CTA"); ladder_note="L0,L1 failed -> L2"
                        if a4.get("certified"): cert_recs=[a4]
                if b==7 and not cert_recs and b6_cert_rung is not None and not SMOKE and el()<HARD_WALL_S:
                    # CT-C: compose the certified b6 rung's output as an input (pre-registered conditional)
                    n6,c6=b6_cert_rung; fin6=CT_FIN[c6]
                    m6=make_rung(n6,fin6,CERT_BLOCK).to('cuda').eval()
                    m6.load_state_dict({k:v.to('cuda') for k,v in BASES[f"sd_b6_{n6}_{c6}_real"].items()})
                    sc6m=BASES[f"scaler_{c6}_b6"]["mean"].to('cuda'); sc6s=BASES[f"scaler_{c6}_b6"]["std"].to('cuda')
                    def obj6hat(cap,ids):
                        fx=contract_feats(c6,cap,ids)
                        return rung_predict(m6,n6,fin6,(fx-sc6m)/sc6s,ids.shape[0])
                    extra={"train":obj6hat(cap_tr,IDS_TRAIN),"sacred":obj6hat(cap_sac,IDS_SACRED),
                           "hold2":obj6hat(cap_h2,IDS_HOLD2)}
                    a5=run_attempt("L0","CTC",extra); ladder_note+=" -> CT-C"
                    if a5.get("certified"): cert_recs=[a5]
                    del m6,extra; free()
                # band (mechanical)
                done_recs=[r for r in attempts.values() if r.get("done")]
                best=min(done_recs,key=lambda r:r["SACRED_kl_rep"]) if done_recs else None
                if cert_recs:
                    best=cert_recs[0]
                    band="CERTIFIES" if best["rung"]=="L0" else "CERTIFIES-NONLINEAR"
                elif best is not None:
                    kl=best["SACRED_kl_rep"]
                    if kl<=0.9*wall and kl<best["twin_kl_rep"] and kl<0.9*W0b: band="PARTIAL"
                    else: band="FAILS-HONESTLY"
                else: band="NOT-RUN"
                brec.update({"done":True,"H_V7_B":band,"ladder":ladder_note,
                    "best":{"rung":best["rung"],"contract":best["contract"],"SACRED_kl_rep":best["SACRED_kl_rep"],
                            "twin":best["twin_kl_rep"],"HOLD2":best["HOLD2_kl_rep"]} if best else None,
                    "floor_recal":fl_rec,"floor_legacy":fl_leg,"wall_S4":wall,"silent":W0b,
                    "bands":"CERTIFIES <=floor & <=0.5*twin / PARTIAL <=0.9*wall & <twin & <0.9*silent / FAILS-HONESTLY",
                    "bet":("FAILS 45 / CERT 35 / PARTIAL 20" if b==6 else "FAILS 55 / CERT 25 / PARTIAL 20")})
                # failure branch: KL-finetune if PARTIAL and <=2*floor
                if band=="PARTIAL" and best and best["SACRED_kl_rep"]<=2*fl_rec and not brec.get("finetune") and el()<HARD_WALL_S:
                    logln(f"==== armB b{b} FAILURE BRANCH: KL-finetune {best['rung']}_{best['contract']} ====")
                    name,ct=best["rung"],best["contract"]; fin=CT_FIN[ct]
                    mF=make_rung(name,fin,CERT_BLOCK).to('cuda').train()
                    mF.load_state_dict({k:v.to('cuda') for k,v in BASES[f"sd_b{b}_{name}_{ct}_real"].items()})
                    fb=feats_sets(ct)
                    optf=torch.optim.Adam(mF.parameters(),lr=FT_LR)
                    fbk=fb["train"].reshape(Ntr,CERT_BLOCK,fin); obk=obj_by_set["train"].reshape(Ntr,CERT_BLOCK,d)
                    yc_cache=ycl("train",IDS_TRAIN); fl_curve=[]
                    for st in range(FT_STEPS):
                        optf.zero_grad(set_to_none=True); lo=0.0
                        for ci,s0 in enumerate(range(0,Ntr,MB)):
                            s1=min(Ntr,s0+MB)
                            if name=="L2": raw=mF(fbk[s0:s1]).reshape(-1,d)
                            else: raw=mF(fbk[s0:s1].reshape(-1,fin))
                            oh=proj_compl(raw); objc=obk[s0:s1].reshape(-1,d)
                            delta=(oh-objc).reshape(s1-s0,CERT_BLOCK,d).clone(); delta[:, :IND_SEG, :]=0.0
                            injb.add=delta; injb.on=True
                            lg=M["m"](IDS_TRAIN[s0:s1].to('cuda'),use_cache=False).logits; injb.on=False; injb.add=None
                            yc=yc_cache[ci].float()
                            logp=Fnn.log_softmax(yc,-1); p=logp.exp(); lp=Fnn.log_softmax(lg.float(),-1)
                            kl=(p*(logp-lp)).sum(-1)[:,IND_SEG:CERT_BLOCK].mean()
                            (kl*(s1-s0)/Ntr).backward(); lo+=float(kl.item())*(s1-s0)/Ntr
                        optf.step(); fl_curve.append(lo)
                        if (st+1)%max(1,FT_STEPS//10)==0: logln(f"[FT b{b}] step {st+1}/{FT_STEPS} trainKL={lo:.5f}")
                    mF.eval()
                    oh_s=rung_predict(mF,name,fin,fb["sacred"],N_SACRED)
                    sub_s=substitution_kl_at(b,oh_s,obj_by_set["sacred"],IDS_SACRED,ycl("sacred",IDS_SACRED),injb,want_behav=True)
                    ftc=bool(sub_s["kl_rep"]<=fl_rec)
                    BASES[f"sd_b{b}_{name}_{ct}_ft"]={k:v.detach().cpu() for k,v in mF.state_dict().items()}; save_bases()
                    brec["finetune"]={"rung":name,"contract":ct,"SACRED_kl_rep":sub_s["kl_rep"],
                                      "certified_via_ft":ftc,"behav":sub_s.get("behav")}
                    if ftc:
                        brec["H_V7_B"]="CERTIFIES-VIA-KL-FINETUNE"
                        brec["best"]={"rung":name,"contract":ct,"SACRED_kl_rep":sub_s["kl_rep"],
                                      "twin":best["twin_kl_rep"],"HOLD2":None,"via":"KL-finetune"}
                    del mF,fb,fbk,obk; free()
                armb[str(b)]=brec; res["armB"]["bounds"]=armb; write_json()
                logln(f"[armB b{b}] H-V7-B={brec['H_V7_B']} best={brec.get('best')}")
                if b==6 and brec["H_V7_B"].startswith("CERTIFIES") and brec.get("best",{}) and brec["best"].get("rung")=="L0":
                    b6_cert_rung=(brec["best"]["rung"],brec["best"]["contract"])
                injb.close()
                del obj_by_set; free()
            res["armB"]["done"]=True; write_json()
        YCL={"train":None,"sacred":None,"hold2":None}; free()

    # =================================================================================
    # VERDICT -- H-OPEN6-a VERBATIM, BOTH METERS (recal primary), V7 grain overrides
    # =================================================================================
    if not SMOKE and not res["verdict"].get("done"):
        allcells=[(r,b) for r in REGIMES for b in range(nL+1)]
        c1band=res["c1"].get("H_V7_C1")
        armaC=res["armA"].get("cells",{})
        armbB=res["armB"].get("bounds",{})
        def vgrain(key):
            cell=v3cells[key]; kl=cell["KL"]["S7"]; grain="S7"
            if key=="repetition_b5":
                if c1band=="FAILS": kl=WALL_S4_B5; grain="S4-wall(C1-FAILS,rescoped)"
                else: kl=S9X_SACRED; grain="S9x-surrogate(L0,V6,C1-"+str(c1band)+")"
            for bb in (6,7):
                if key==f"repetition_b{bb}":
                    rec=armbB.get(str(bb),{})
                    if rec.get("H_V7_B","").startswith("CERTIFIES") and rec.get("best"):
                        kl=rec["best"]["SACRED_kl_rep"]; grain=f"S9x-onset({rec['best']['rung']},{rec['best']['contract']})"
            for bb in (8,9,10,11):
                if key==f"repetition_b{bb}": kl=V6_R48_REP[bb]; grain="S7-r48-folded(carried V6)"
            if key=="repetition_b12": kl=B12_R48_BANK; grain="S7-r48-folded(carried V5)"
            rec=armaC.get(key)
            if rec and rec.get("done") and rec.get("gates_ok") and rec.get("KL_r48") is not None:
                kl=rec["KL_r48"]; grain="S7-r48-folded(V7)"
            return kl,grain
        tables={}
        for meter in ("legacy","recal"):
            tab={}; N_open=0; N_grain=0; gaps=[]
            for (r,b) in allcells:
                key=f"{r}_b{b}"; cell=v3cells[key]
                if meter=="legacy": fl=floors_leg[b][r]
                else:
                    fl=floors_rec[b].get(r) if r!="prose" else 0.1871
                    if fl is None or not RECAL_OK: fl=floors_leg[b][r]
                kl,grain=vgrain(key)
                p_open=bool(cell["KL"]["S2w"]<=fl); p_grain=bool(kl<=fl)
                if p_open: N_open+=1
                if p_grain: N_grain+=1
                else: gaps.append({"cell":key,"grain":grain,"KL":round(kl,5),"floor":round(fl,5),
                                   "excess_nats":round(kl-fl,5),"ratio":round(kl/fl,2)})
                tab[key]={"KL":round(kl,5),"grain":grain,"floor":round(fl,5),"pass_open":p_open,"pass_grain":p_grain}
            gaps.sort(key=lambda x:-x["excess_nats"])
            tables[meter]={"cells":tab,"N_open":N_open,"N_grain":N_grain,"gap_cells":len(gaps),
                           "unexplained_nats":round(sum(g["excess_nats"] for g in gaps),3),"gap_table":gaps}
        primary="recal" if RECAL_OK else "legacy"
        pt=tables[primary]
        if pt["N_open"]==39: Ha="OPEN"
        elif pt["N_grain"]==39: Ha="OPEN-AT-GRAIN"
        else: Ha="NOT-YET"
        res["verdict"]={"done":True,"H_V7_VERDICT":Ha,"primary_meter":primary,"tables":tables,
            "c1_band":c1band,"c2_band":res["c2"].get("H_V7_C2"),
            "armA_closures":{k:v.get("H_V7_A") for k,v in armaC.items()},
            "armB_bands":{k:v.get("H_V7_B") for k,v in armbB.items()},
            "verdict_bet":"NOT-YET 90 / OPEN-AT-GRAIN 9 / OPEN 1","g_room":0.8614,
            "escalation":("band MET -> program-complete recommendation + STOP, Will ratifies" if Ha=="OPEN-AT-GRAIN"
                          else "NOT-YET -> gap tables (both meters) + fork if onset-only + STOP, Will decides")}
        write_json()
        logln(f"[VERDICT] primary={primary} H-V7={Ha} | recal N_grain={tables['recal']['N_grain']} "
              f"gaps={tables['recal']['gap_cells']} unexpl={tables['recal']['unexplained_nats']} | "
              f"legacy N_grain={tables['legacy']['N_grain']} gaps={tables['legacy']['gap_cells']} "
              f"unexpl={tables['legacy']['unexplained_nats']}")

    # ---- freeze decoder_v7 IFF any onset boundary certified (pre-reg clause) ----
    certB=[bb for bb in ("6","7") if res["armB"].get("bounds",{}).get(bb,{}).get("H_V7_B","").startswith("CERTIFIES")]
    if not SMOKE and certB and not res.get("v7_frozen"):
        v7T=dict(dv6)
        for bb in certB:
            rec=res["armB"]["bounds"][bb]["best"]
            name,ct=rec["rung"],rec["contract"]
            sdk=f"sd_b{bb}_{name}_{ct}_"+("ft" if rec.get("via")=="KL-finetune" else "real")
            v7T[f"onset_b{bb}_rung"]=name; v7T[f"onset_b{bb}_contract"]=ct
            v7T[f"onset_b{bb}_state_dict"]=BASES[sdk]
            v7T[f"onset_b{bb}_scaler_mean"]=BASES[f"scaler_{ct}_b{bb}"]["mean"]
            v7T[f"onset_b{bb}_scaler_std"]=BASES[f"scaler_{ct}_b{bb}"]["std"]
        for k in list(BASES.keys()):
            if str(k).startswith("O_r48_"): v7T[k]=BASES[k]
        tmp=os.path.join(DIR,"decoder_v7_tensors.pt.tmp"); torch.save(v7T,tmp); os.replace(tmp,os.path.join(DIR,"decoder_v7_tensors.pt"))
        cfg={"version":"DECODER_V7 1.0 (2026-07-05)","propose_only":True,"pre_registration":PEN,
             "assembly":"decoder_v6 + S9x onset rung(s) at BUS[6]/BUS[7] (certified on held-out periods) + V7 folded r48 reads",
             "onset":{bb:res["armB"]["bounds"][bb]["best"] for bb in certB},
             "source_sha256":O["src_sha"]}
        tmp=os.path.join(DIR,"decoder_v7.json.tmp")
        with open(tmp,"w",encoding="utf-8") as f: json.dump(cfg,f,indent=1,default=str)
        os.replace(tmp,os.path.join(DIR,"decoder_v7.json"))
        res["v7_frozen"]={"tensors_sha":sha256(os.path.join(DIR,"decoder_v7_tensors.pt")),
                          "json_sha":sha256(os.path.join(DIR,"decoder_v7.json"))}
        write_json(); logln(f"[FREEZE] DECODER_V7 frozen: {res['v7_frozen']}")

    # ================= SMOKE / STATUS =================
    if SMOKE:
        sm={"M0a":res["gates"]["M0a"]["pass"],"dec_v6":res["gates"]["decoder_v6"]["sha_ok"],
            "b5_gates_id":res["gates"].get("b5",{}).get("identity_kl"),
            "c1":bool(res["c1"].get("done")),"armA":bool(res["armA"].get("done")),
            "c2":bool(res["c2"].get("done")),"armB":bool(res["armB"].get("done"))}
        ok=(res["gates"]["M0a"]["pass"] and res["gates"]["decoder_v6"]["sha_ok"]
            and res["gates"].get("b5",{}).get("identity_kl")==0.0
            and all(bool(sm[k]) for k in ("c1","armA","c2","armB")))
        res["S_smoke"]=sm; res["status"]="SMOKE-"+("OK" if ok else "FAIL")
        logln(f"[SMOKE] {json.dumps(sm)} -> {res['status']}")
    else:
        done=(bool(res["c1"].get("done")) and bool(res["armA"].get("done"))
              and bool(res["c2"].get("done")) and bool(res["armB"].get("done")) and bool(res["verdict"].get("done")))
        res["status"]=("COMPLETE" if (done and not res["instrument_discrepancy"]) else
                       ("COMPLETE-WITH-DISCREPANCY" if done else "PARTIAL"))
    save_bases(); write_json()
    if M["m"] is not None: del M["m"]; M["m"]=None; free()
except Exception as e:
    res["fatal_error"]={"error":str(e),"trace":traceback.format_exc()}
    logln(f"FATAL {e}\n{traceback.format_exc()}"); res.setdefault("status","FATAL")
write_json()
logln(f"V7 END status={res.get('status')} elapsed={el()}s")
open(os.path.join(DIR,"_v7_smoke_gpu.done" if SMOKE else "_v7_gpu.done"),"w").write(str(res.get("status","?"))+"\n")
logln("*** V7_"+("SMOKE_" if SMOKE else "")+"DONE ***"); LOG.flush(); LOG.close(); print("done")
