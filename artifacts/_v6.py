# _v6.py -- V6 TEACH THE WALL'S STUDENT (FQ-16 SURROGATE DISTILLATION AT REP-B5). GPT-2 124M. PROPOSE-ONLY.
# Pre-registration: FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md ::
#   "V6 -- TEACH THE WALL'S STUDENT (FQ-16 SURROGATE DISTILLATION AT REP-B5) -- GAP-SCAN + PRE-REGISTRATION (2026-07-05 ~20:10)"
# Brief: V6_BRIEF_2026-07-05.md (Will "do 2. ultrathink"). Doctrine: plan binding, propose-only,
#   bands SHARPENED never weakened, escalation binding, both-meter reporting permanent, recal PRIMARY.
# MACHINERY reused VERBATIM from _v5.py: model loader / capture / KL / InjectHook / inject_kl_full /
#   inject_kl_pidx / HeadHook / MLPHook / write_svd / load_objects+M0a gate / s4_delta / Arm-B(b12) recipe.
# NEW code: capture_feats (H2,H5,wm0), surrogate ladder (Linear/MLP/Attn), MSE training + shuffled-target
#   twins, substitution certification at BUS[5] (delta=obj_hat-obj_true), behavioral leg, Arm B folded
#   r48 at b8..b11, Arm C code-column probe, both-meter verdict recompute, decoder_v6 freeze iff certified.
import json, time, os, math, traceback, gc, subprocess, hashlib, ctypes
import torch, torch.nn as nn, torch.nn.functional as Fnn
import torch.nn.functional as F

t0=time.time()
DIR=r"C:\Shadow\Dissector\D0_PROGRAM\CONSTRUCTIVE"
SMOKE=os.environ.get("V6_SMOKE")=="1"
LOG=open(os.path.join(DIR,"_v6.log"),"a",encoding="utf-8")
def logln(s):
    s=str(s); LOG.write(f"[V6 {round(time.time()-t0,1):8.1f}s] "+s+"\n"); LOG.flush()
    try: print(s,flush=True)
    except Exception: pass
def el(): return round(time.time()-t0,1)
logln("="*100); logln(f"V6 START smoke={SMOKE} torch={torch.__version__}")
try:
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(),0x4000)
    logln("[ops] priority BelowNormal set")
except Exception as e: logln(f"[ops] priority set failed: {e}")
torch.set_num_threads(6)

# ---------------- locked constants ----------------
EPS_KL=0.1871; EPS_MSE=0.080085; CERT_BLOCK=512; IND_SEG=64; MB=4; CAP_CHUNK=16
VOCAB_SANS_SPECIALS=50256; REGIMES=["prose","code","repetition"]
ORIG_LO,ORIG_HI=8192,16384; FRESH_LO,FRESH_HI=24576,32768
REP_SEED=3; SEED_J=20260705
B2b=2; B5=5; D_COMPL=364
NAMED_HEADS=[(0,1),(0,5),(1,7),(1,4),(2,10)]; NCOMP_LAYERS=[0,1,2,3,4]
# surrogate config
FEAT_DIM=768+768+1
MLP_H=768; ATTN_DM=256; ATTN_HEADS=4; ATTN_NBLK=(1 if SMOKE else 2); ATTN_MLP=2
STEPS=40 if SMOKE else 4000; CKPT_STEPS=20 if SMOKE else 500; LR=1e-3
FT_STEPS=20 if SMOKE else 300; FT_LR=3e-4
N_TRAIN=8 if SMOKE else 96; N_HOLD2=4 if SMOKE else 16; N_SACRED=4 if SMOKE else 16
TRAIN_SEED0=7000; HOLD2_SEED0=8000
P_TRAIN=(64,384); P_WITHIN=(384,512); P_REPERA=(64,512)
# banked anchors (byte-replay before dependent bands)
WALL_S4=3.46003; FLOOR_B5_RECAL=0.1279
V3_S7={"repetition_b8":0.08774,"repetition_b9":0.12328,"repetition_b10":0.21684,
       "repetition_b11":0.45241,"repetition_b12":0.55899,"code_b7":0.50915}
B12_R48_BANK=0.18155  # V5, carried for the b12 verdict cell (already CLOSES-RECAL)
RANKS_ARMB=[20] if SMOKE else [20,48]; ARMB_BOUNDS=[10,11] if SMOKE else [8,9,10,11]
ARMC_CODE_B=7
SOFT_COMPUTE_S=6.0*3600; HARD_WALL_S=int(11.5*3600); ARM_C_GATE_S=3.0*3600
# bands (verdict axis = best-rung SACRED rep-era substitution-KL)
WALL_09=round(0.9*WALL_S4,5)  # 3.11403

RESULT_JSON=os.path.join(DIR,"_v6_result_SMOKE.json" if SMOKE else "_v6_result.json")
BASES_PT=os.path.join(DIR,"_v6_bases_SMOKE.pt" if SMOKE else "_v6_bases.pt")
torch.manual_seed(1234)

PEN=("FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md :: 'V6 -- TEACH THE WALL'S STUDENT (FQ-16 SURROGATE "
     "DISTILLATION AT REP-B5) -- GAP-SCAN + PRE-REGISTRATION (2026-07-05 ~20:10)'")
res={"experiment":"V6 FQ-16 surrogate distillation at rep-b5: architecture ladder (Linear/MLP/Attn) "
     "trained by MSE on the span5-complement object from readable inputs {L2 state, current-token, "
     "m0 k*=1 coeff}, certified by substitution-KL at BUS[5] on held-out repeat PERIODS (SACRED "
     "falsifier), shuffled-target twin nulls per rung; Arm B folded r48 reads rep b8..b11; Arm C "
     "code-column recon; verdict recompute BOTH meters recal primary",
     "date":"2026-07-05","propose_only":True,"pre_registration":PEN,
     "config":{"n_train":N_TRAIN,"n_hold2":N_HOLD2,"n_sacred":N_SACRED,"steps":STEPS,"lr":LR,
        "mlp_h":MLP_H,"attn_dm":ATTN_DM,"attn_heads":ATTN_HEADS,"attn_nblk":ATTN_NBLK,
        "p_train":P_TRAIN,"p_within":P_WITHIN,"floor_b5_recal":FLOOR_B5_RECAL,"wall_s4":WALL_S4,
        "ranks_armb":RANKS_ARMB,"armb_bounds":ARMB_BOUNDS,
        "precision":"fp32","tf32":"off","attn":"eager","seed":1234,"smoke":SMOKE},
     "gpu_free_checks":[],"instrument_discrepancy":[],
     "gates":{},"data":{},"ladder":{},"cert":{},"armB":{},"armC":{},"verdict":{},"status":"INIT"}

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
        for k in ("gates","data","ladder","cert","armB","armC","verdict","gpu_free_checks","instrument_discrepancy"):
            if prev.get(k): res[k]=prev[k]
        logln(f"*** RESUME *** prior elapsed={prev.get('elapsed_s')}")
    except Exception as e: logln(f"resume load fail {e}")
if os.path.exists(BASES_PT):
    try: BASES=torch.load(BASES_PT,map_location="cpu",weights_only=False); logln(f"*** RESUME bases {sorted(map(str,BASES.keys()))[:20]}")
    except Exception as e: logln(f"bases load fail {e}"); BASES={}
write_json()

# ---------------- GPU free-check (verbatim from _v5.py) ----------------
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
    # n distinct repeated segments, each its own 512 block (period 64); seeds seed0..seed0+n-1
    rows=[build_dind(1,CERT_BLOCK,seed0+i) for i in range(n)]
    return torch.cat(rows,0)
def ids_window(all_ids,lo,hi,what):
    if len(all_ids)<hi: raise RuntimeError(f"{what}: {len(all_ids)}<{hi}")
    n=(hi-lo)//CERT_BLOCK; return torch.tensor(all_ids[lo:hi],dtype=torch.long).view(n,CERT_BLOCK)

# ---------------- objects + M0a content gate (VERBATIM from _v5.py) ----------------
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
             "_open1_bases.pt","_open5_result.json","_v5_bases.pt","_v5_floors_recal.json","_v3_result.json")}
    return dict(C=C,mu=mu,B2=B2,U=U,V35=V35,Q35=Q35,frozen=frozen,floors=floors,mstars=mstars,
                wte_W=wte_W,wte_c=wte_c,src_sha=src_sha)

# ---------------- captures / KL / inject (VERBATIM from _v5.py) ----------------
def center(z): return z - z.mean(-1,keepdim=True)
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
def write_svd(r, d):
    rf=r.detach().float().reshape(-1,d)
    try:
        U,S,Vh=torch.linalg.svd(rf,full_matrices=False); return Vh
    except Exception as e:
        logln(f"[svd] fallback random basis ({e})"); Q,_=torch.linalg.qr(torch.randn(d,d,device=r.device)); return Q.t()

# ---------------- NEW: feature capture ----------------
def capture_feats(ids_cpu,tag):
    # returns H2,H5,wm0 (Ntok x d) on CPU
    model=M["m"]; N=ids_cpu.shape[0]; d=M["d"]; buf={}
    def mk2(m,i,o): buf['h2']=(o[0] if isinstance(o,tuple) else o).detach()
    def mk5(m,i,o): buf['h5']=(o[0] if isinstance(o,tuple) else o).detach()
    def mkm(m,i,o): buf['wm0']=o.detach()
    hh=[M['blocks'][B2b-1].register_forward_hook(mk2),
        M['blocks'][B5-1].register_forward_hook(mk5),
        M['blocks'][0].mlp.register_forward_hook(mkm)]
    h2=[];h5=[];wm0=[]
    with torch.no_grad():
        for c0 in range(0,N,CAP_CHUNK):
            c1=min(N,c0+CAP_CHUNK); _=model(ids_cpu[c0:c1].to('cuda'),use_cache=False)
            h2.append(buf['h2'].reshape(-1,d).cpu()); h5.append(buf['h5'].reshape(-1,d).cpu()); wm0.append(buf['wm0'].reshape(-1,d).cpu())
    for x in hh: x.remove()
    logln(f"[feats {tag}] N={N} blocks captured")
    return torch.cat(h2),torch.cat(h5),torch.cat(wm0)

# ---------------- NEW: surrogate ladder ----------------
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
def make_rung(name,seqlen):
    if name=="L0": return LinearRung(FEAT_DIM,M["d"])
    if name=="L1": return MLPRung(FEAT_DIM,MLP_H,M["d"])
    if name=="L2": return AttnRung(FEAT_DIM,ATTN_DM,ATTN_HEADS,ATTN_NBLK,ATTN_MLP,M["d"],seqlen)
    raise ValueError(name)

# ======================================================================================
# MAIN
# ======================================================================================
try:
    ensure_model()
    O=load_objects()
    if not res["gates"]["M0a"]["pass"]:
        res["status"]="STOPPED-GATE"; write_json(); raise RuntimeError("FB: M0a breach -> STOP")
    d=M["d"]; nL=M["nL"]; nH=M["nH"]; hd=d//nH
    B2_g=O["B2"].to('cuda'); Q35_g=O["Q35"].to('cuda'); span5=torch.cat([B2_g,Q35_g],1)
    mu_all=O["mu"]  # (13,768)
    mu2=mu_all[B2b].to('cuda'); mu5=mu_all[B5].to('cuda')
    wteW_g=O["wte_W"].to('cuda'); wtec_g=O["wte_c"].to('cuda')
    wte_g=M["wte"].detach().float()
    v5b=torch.load(os.path.join(DIR,"_v5_bases.pt"),map_location="cpu",weights_only=False)
    Vk=v5b["m0_repera_Vk_recal"].to('cuda')  # 768x1 certified k*=1 basis
    logln(f"[objects] span5 {tuple(span5.shape)} mu {tuple(mu_all.shape)} Vk {tuple(Vk.shape)} B2 {tuple(B2_g.shape)} Q35 {tuple(Q35_g.shape)}")
    frec=json.load(open(os.path.join(DIR,"_v5_floors_recal.json"),encoding="utf-8"))
    floors_leg={int(b):{k:float(v) for k,v in frec["floors_legacy"][str(b)].items()} for b in range(13)}
    floors_rec={int(b):{k:(float(v) if v is not None else None) for k,v in frec["floors_recal"][str(b)].items()} for b in range(13)}
    RECAL_OK=(not frec.get("quarantined")) and frec.get("sg_early_ok") and frec.get("repl_all")
    logln(f"[floors] recal b5 rep={floors_rec[5]['repetition']} RECAL_OK={RECAL_OK}")

    WIKI=M["tok"](load_wiki_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
    def s4_delta(Xc,b,Ecur_all):
        b2P=(Xc@B2_g)@B2_g.t(); q35P=(Xc@Q35_g)@Q35_g.t()
        yhat=Ecur_all@wteW_g[b].t()+wtec_g[b]
        y2=yhat-(yhat@B2_g)@B2_g.t(); y4=y2-(y2@Q35_g)@Q35_g.t()
        return b2P+q35P+y4-Xc

    # streams
    IDS_TRAIN=build_dind_seeds(TRAIN_SEED0,N_TRAIN)
    IDS_SACRED=build_dind(N_SACRED,CERT_BLOCK,REP_SEED)
    IDS_HOLD2=build_dind_seeds(HOLD2_SEED0,N_HOLD2)
    def proj_compl(x): return x-(x@span5)@span5.t()
    def make_feats_and_obj(ids_cpu,tag):
        H2,H5,wm0=capture_feats(ids_cpu,tag)
        x2=(H2.to('cuda')-mu2); Xc5=H5.to('cuda')-mu5
        obj=proj_compl(Xc5)
        ecur=wte_g[ids_cpu.reshape(-1).to('cuda')]
        s=wm0.to('cuda')@Vk
        feats=torch.cat([x2,ecur,s],1)
        return feats.cpu(),obj.cpu(),Xc5.cpu()

    # =================================================================================
    # STAGE 0 -- capture datasets, build scaler (resume-safe)
    # =================================================================================
    if not res["data"].get("done"):
        gpu_free_check("capture")
        logln("==== STAGE 0: capture datasets + scaler ====")
        ft_tr,obj_tr,_=make_feats_and_obj(IDS_TRAIN,"train")
        BASES["feats_train"]=ft_tr; BASES["obj_train"]=obj_tr; save_bases()
        # scaler from TRAIN rep-era positions [64,384)
        Ntr=IDS_TRAIN.shape[0]
        maskrows=torch.zeros(Ntr,CERT_BLOCK,dtype=torch.bool); maskrows[:,P_TRAIN[0]:P_TRAIN[1]]=True
        mrow=maskrows.reshape(-1)
        tr_rep=ft_tr[mrow]
        sc_mean=tr_rep.mean(0,keepdim=True); sc_std=tr_rep.std(0,keepdim=True).clamp(min=1e-6)
        BASES["sc_mean"]=sc_mean; BASES["sc_std"]=sc_std; save_bases()
        res["data"]={"done":True,"n_train":Ntr,"n_train_reptok":int(mrow.sum()),
                     "feat_dim":FEAT_DIM,"obj_dim":d,
                     "obj_train_var":float(((obj_tr[mrow]-obj_tr[mrow].mean(0))**2).sum().item()),
                     "note":"feats=[x2(L2 centered),ecur(wte),s(m0 k*=1 coeff)]; obj=span5-complement at BUS5; "
                            "scaler from TRAIN rep-era [64,384)"}
        write_json(); logln(f"[data] train reptok={int(mrow.sum())} feat_dim={FEAT_DIM}")
        del tr_rep; free()
    sc_mean=BASES["sc_mean"].to('cuda'); sc_std=BASES["sc_std"].to('cuda')
    ft_tr=BASES["feats_train"]; obj_tr=BASES["obj_train"]
    Ntr=IDS_TRAIN.shape[0]
    def scale(f): return (f-sc_mean)/sc_std

    # training-row selection (per-token) and block form (attn)
    maskrows=torch.zeros(Ntr,CERT_BLOCK,dtype=torch.bool); maskrows[:,P_TRAIN[0]:P_TRAIN[1]]=True
    mrow=maskrows.reshape(-1); mrow_g=mrow.to('cuda')
    feats_tr_g=scale(ft_tr.to('cuda'))          # (Ntok,F)
    obj_tr_g=obj_tr.to('cuda')                  # (Ntok,d)
    feats_tr_rep=feats_tr_g[mrow_g]; obj_tr_rep=obj_tr_g[mrow_g]
    # block form for attention
    feats_tr_blk=feats_tr_g.reshape(Ntr,CERT_BLOCK,FEAT_DIM)
    obj_tr_blk=obj_tr_g.reshape(Ntr,CERT_BLOCK,d)
    mask_blk=maskrows.to('cuda')
    BCHUNK=8 if SMOKE else 32          # block-chunk for L2 grad-accumulation (OOM-safe, deterministic)
    RUNG_SEED={"L0":11,"L1":22,"L2":33}

    # =================================================================================
    # STAGE 1 -- train the ladder (each rung: real + shuffled twin)
    # =================================================================================
    def train_rung(name,shuffle,steps,tag):
        torch.manual_seed(20260706 + (1 if shuffle else 0) + RUNG_SEED[name])
        model=make_rung(name,CERT_BLOCK).to('cuda').train()
        opt=torch.optim.Adam(model.parameters(),lr=LR)
        losses=[]
        # targets
        if name=="L2":
            tgt=obj_tr_blk
            if shuffle:
                # permute rep-era targets across the flattened rep rows, scatter back into block form
                idx=torch.randperm(int(mrow.sum()),device='cuda')
                permd=obj_tr_rep[idx]
                tgt=obj_tr_blk.clone(); tgt.reshape(-1,d)[mrow_g]=permd
            n_elem=float(mask_blk.sum().item()*d)
        else:
            tgt=obj_tr_rep
            if shuffle:
                idx=torch.randperm(tgt.shape[0],device='cuda'); tgt=tgt[idx]
        for step in range(steps):
            opt.zero_grad(set_to_none=True)
            if name=="L2":
                acc=0.0
                for c0 in range(0,Ntr,BCHUNK):
                    c1=min(Ntr,c0+BCHUNK)
                    raw=model(feats_tr_blk[c0:c1])             # (bc,512,d)
                    oh=proj_compl(raw.reshape(-1,d)).reshape(c1-c0,CERT_BLOCK,d)
                    err=(oh-tgt[c0:c1])[mask_blk[c0:c1]]
                    loss=(err*err).sum()/n_elem                # sum of chunk losses = full-batch mean
                    loss.backward(); acc+=float(loss.item())
                losses.append(acc)
            else:
                raw=model(feats_tr_rep)
                oh=proj_compl(raw)
                err=oh-tgt; loss=(err*err).mean()
                loss.backward(); losses.append(float(loss.item()))
            opt.step()
            if (step+1)%CKPT_STEPS==0 or step==steps-1:
                BASES[f"sd_{tag}"]={k:v.detach().cpu() for k,v in model.state_dict().items()}
                BASES[f"step_{tag}"]=step+1; save_bases()
                logln(f"[train {tag}] step {step+1}/{steps} loss={losses[-1]:.5f}")
        return model,losses

    LAD=res["ladder"]
    RUNGS=["L0","L1"] if SMOKE else ["L0","L1","L2"]
    rung_models={}
    for name in RUNGS:
        if LAD.get(name,{}).get("done"):
            logln(f"[ladder {name}] SKIP (resume)")
            m=make_rung(name,CERT_BLOCK).to('cuda').eval(); m.load_state_dict({k:v.to('cuda') for k,v in BASES[f"sd_{name}_real"].items()})
            rung_models[name]=m; continue
        if el()>HARD_WALL_S: logln("[FB-WALL] ladder stopped"); break
        gpu_free_check(f"train_{name}")
        mr,lr_=train_rung(name,False,STEPS,f"{name}_real")
        mt,lt_=train_rung(name,True,STEPS,f"{name}_twin")
        rung_models[name]=mr.eval()
        # train/within R2 for the REAL rung
        with torch.no_grad():
            if name=="L2":
                oh=proj_compl(mr(feats_tr_blk).reshape(-1,d))
            else:
                oh=proj_compl(mr(feats_tr_g))
            def r2(mask):
                e=((oh[mask]-obj_tr_g[mask])**2).sum(); v=((obj_tr_g[mask]-obj_tr_g[mask].mean(0))**2).sum()
                return float(1-(e/v.clamp(min=1e-9)))
            r2_train=r2(mrow)
            mwith=torch.zeros(Ntr,CERT_BLOCK,dtype=torch.bool); mwith[:,P_WITHIN[0]:P_WITHIN[1]]=True
            r2_within=r2(mwith.reshape(-1).to('cuda'))
        LAD[name]={"done":True,"params":n_params(mr),"loss_curve":[round(x,6) for x in lr_[::max(1,len(lr_)//40)]],
                   "twin_loss_curve":[round(x,6) for x in lt_[::max(1,len(lt_)//40)]],
                   "final_loss_real":round(lr_[-1],6),"final_loss_twin":round(lt_[-1],6),
                   "r2_train":round(r2_train,4),"r2_within":round(r2_within,4)}
        res["ladder"]=LAD; write_json()
        logln(f"[ladder {name}] params={n_params(mr)} loss_real={lr_[-1]:.5f} loss_twin={lt_[-1]:.5f} r2_train={r2_train:.4f} r2_within={r2_within:.4f}")

    # =================================================================================
    # STAGE 2 -- certify each rung: substitution-KL at BUS[5] on the eval sets
    # =================================================================================
    inj5=InjectHook(M["blocks"][B5-1])
    pidx_rep=torch.arange(IND_SEG,CERT_BLOCK)
    def run_surrogate(name,model,ids_cpu,tag):
        feats,obj,Xc5=make_feats_and_obj(ids_cpu,tag)
        N=ids_cpu.shape[0]; feats_g=scale(feats.to('cuda')); obj_g=obj.to('cuda')
        with torch.no_grad():
            if name=="L2":
                raw=model(feats_g.reshape(N,CERT_BLOCK,FEAT_DIM)).reshape(-1,d)
            else:
                raw=model(feats_g)
            oh=proj_compl(raw)
        return oh,obj_g,N
    def substitution_kl(oh,obj_g,ids_cpu,tag,want_behav=False):
        N=ids_cpu.shape[0]
        delta=(oh-obj_g).reshape(N,CERT_BLOCK,d).clone(); delta[:, :IND_SEG, :]=0.0
        Ycl=clean_logits(ids_cpu)
        kl_rep=inject_kl_pidx(ids_cpu,inj5,delta,Ycl,pidx_rep)
        kl_all,dl=inject_kl_full(ids_cpu,inj5,delta,Ycl,want_dl=True)
        out={"kl_rep":round(kl_rep,5),"kl_all":round(kl_all,5),"max_dlogit":round(dl,5)}
        if want_behav:
            out["behav"]=behav_meter(oh,obj_g,ids_cpu,Ycl)
        return out
    def r2_of(oh,obj_g,ids_cpu):
        N=ids_cpu.shape[0]
        m=torch.zeros(N,CERT_BLOCK,dtype=torch.bool); m[:,IND_SEG:CERT_BLOCK]=True; m=m.reshape(-1).to('cuda')
        e=((oh[m]-obj_g[m])**2).sum(); v=((obj_g[m]-obj_g[m].mean(0))**2).sum()
        return float(1-(e/v.clamp(min=1e-9)))
    def behav_meter(oh,obj_g,ids_cpu,Ycl):
        # copy fidelity: prob of the TRUE next token at rep-era positions [64,510], clean vs substituted
        N=ids_cpu.shape[0]
        delta=(oh-obj_g).reshape(N,CERT_BLOCK,d).clone(); delta[:, :IND_SEG, :]=0.0
        pc=0.0;ps=0.0;ac=0.0;as_=0.0;cnt=0;ci=0
        with torch.no_grad():
            for s0 in range(0,N,MB):
                s1=min(N,s0+MB)
                inj5.add=delta[s0:s1]; inj5.on=True
                lg=M["m"](ids_cpu[s0:s1].to('cuda'),use_cache=False).logits.float(); inj5.on=False; inj5.add=None
                yc=Ycl[ci].float()
                nxt=ids_cpu[s0:s1,IND_SEG+1:CERT_BLOCK].to('cuda')       # (b,447)
                lc=yc[:,IND_SEG:CERT_BLOCK-1]; lsb=lg[:,IND_SEG:CERT_BLOCK-1]
                pcl=Fnn.softmax(lc,-1).gather(-1,nxt[...,None]).squeeze(-1)
                psb=Fnn.softmax(lsb,-1).gather(-1,nxt[...,None]).squeeze(-1)
                pc+=float(pcl.sum()); ps+=float(psb.sum())
                ac+=float((lc.argmax(-1)==nxt).sum()); as_+=float((lsb.argmax(-1)==nxt).sum())
                cnt+=nxt.numel(); ci+=1; del lg
        pc/=cnt; ps/=cnt; ac/=cnt; as_/=cnt
        return {"p_true_clean":round(pc,5),"p_true_sub":round(ps,5),"copy_fidelity_ratio":round(ps/max(pc,1e-9),4),
                "argmax_copy_clean":round(ac,4),"argmax_copy_sub":round(as_,4),"n":cnt}

    if not res["cert"].get("done") and rung_models and el()<HARD_WALL_S:
        gpu_free_check("certify")
        logln("==== STAGE 2: certification (substitution-KL on held-out periods) ====")
        C=res["cert"]
        # instrument gates on SACRED set: identity, S4 byte-replay, SILENT
        if not C.get("gates"):
            feats,obj,Xc5=make_feats_and_obj(IDS_SACRED,"sacred-gate")
            Xc5_g=Xc5.to('cuda'); obj_g=obj.to('cuda'); N=IDS_SACRED.shape[0]
            Ycl=clean_logits(IDS_SACRED)
            zero=torch.zeros(N,CERT_BLOCK,d,device='cuda')
            kl_id,dl_id=inject_kl_full(IDS_SACRED,inj5,zero,Ycl,want_dl=True)
            # S4 byte-replay (all positions, V5 recipe)
            Ecur=wte_g[IDS_SACRED.reshape(-1).to('cuda')]
            dd_S4=s4_delta(Xc5_g,B5,Ecur).reshape(N,CERT_BLOCK,d)
            kl_S4=inject_kl_full(IDS_SACRED,inj5,dd_S4,Ycl)
            # SILENT (obj_hat=0 at rep-era): delta=-obj, masked
            dsil=(-obj_g).reshape(N,CERT_BLOCK,d).clone(); dsil[:, :IND_SEG, :]=0.0
            kl_sil_rep=inject_kl_pidx(IDS_SACRED,inj5,dsil,Ycl,pidx_rep)
            kl_sil_all=inject_kl_full(IDS_SACRED,inj5,dsil,Ycl)
            s4_ok=(abs(kl_S4-WALL_S4)<=2e-3 and kl_id==0.0 and dl_id==0.0) if not SMOKE else (kl_id==0.0)
            if not s4_ok: res["instrument_discrepancy"].append({"stage":"byte-replay","name":"sacred_S4/id","why":{"S4":kl_S4,"id":kl_id,"dl":dl_id}})
            cos_vk=float((Vk[:,0]@v5b["m0_repera_Vk_recal"].to('cuda')[:,0]).abs())
            C["gates"]={"identity_kl":kl_id,"identity_dlogit":dl_id,"S4_replay":round(kl_S4,5),"S4_banked":WALL_S4,
                        "S4_ok":bool(s4_ok),"silent_rep":round(kl_sil_rep,5),"silent_all":round(kl_sil_all,5),
                        "vk_cos_selfcheck":round(cos_vk,6)}
            res["cert"]=C; write_json()
            logln(f"[cert gates] id={kl_id}/{dl_id} S4={kl_S4:.5f}(bk {WALL_S4}) SILENT rep={kl_sil_rep:.5f} all={kl_sil_all:.5f} -> {'OK' if s4_ok else 'FAIL'}")
            del Xc5_g,obj_g,dd_S4; free()
        W0=res["cert"]["gates"]["silent_rep"]
        # per-rung certification
        rungrec=C.get("rungs",{})
        for name in RUNGS:
            if name not in rung_models: continue
            if rungrec.get(name,{}).get("done"): continue
            if el()>HARD_WALL_S: break
            m=rung_models[name]
            # SACRED (held-out period), primary
            oh_s,obj_s,_=run_surrogate(name,m,IDS_SACRED,f"cert-sacred-{name}")
            sub_s=substitution_kl(oh_s,obj_s,IDS_SACRED,f"sacred-{name}",want_behav=True)
            r2_s=r2_of(oh_s,obj_s,IDS_SACRED)
            # SACRED restricted to trained-position range [64,384)
            N=IDS_SACRED.shape[0]
            delta_pt=(oh_s-obj_s).reshape(N,CERT_BLOCK,d).clone(); delta_pt[:, :IND_SEG, :]=0.0; delta_pt[:,P_TRAIN[1]:,:]=0.0
            Ycl_s=clean_logits(IDS_SACRED)
            kl_sacred_pt=inject_kl_pidx(IDS_SACRED,inj5,delta_pt,Ycl_s,torch.arange(IND_SEG,P_TRAIN[1]))
            # HOLD2 (second held-out-period set)
            oh_h,obj_h,_=run_surrogate(name,m,IDS_HOLD2,f"cert-hold2-{name}")
            sub_h=substitution_kl(oh_h,obj_h,IDS_HOLD2,f"hold2-{name}")
            r2_h=r2_of(oh_h,obj_h,IDS_HOLD2)
            # WITHIN-seen-position on TRAIN blocks (secondary axis): substitute only [384,512)
            oh_t,obj_t,_=run_surrogate(name,m,IDS_TRAIN,f"cert-within-{name}")
            Nt=IDS_TRAIN.shape[0]
            dW=(oh_t-obj_t).reshape(Nt,CERT_BLOCK,d).clone(); dW[:, :P_WITHIN[0], :]=0.0
            Ycl_t=clean_logits(IDS_TRAIN)
            kl_within=inject_kl_pidx(IDS_TRAIN,inj5,dW,Ycl_t,torch.arange(P_WITHIN[0],CERT_BLOCK))
            # TWIN on SACRED
            mt=make_rung(name,CERT_BLOCK).to('cuda').eval(); mt.load_state_dict({k:v.to('cuda') for k,v in BASES[f"sd_{name}_twin"].items()})
            oh_tw,obj_tw,_=run_surrogate(name,mt,IDS_SACRED,f"cert-twin-{name}")
            sub_tw=substitution_kl(oh_tw,obj_tw,IDS_SACRED,f"twin-{name}")
            r2_tw=r2_of(oh_tw,obj_tw,IDS_SACRED)
            twin_kl=sub_tw["kl_rep"]; real_kl=sub_s["kl_rep"]
            beats_twin=bool(real_kl<=0.5*twin_kl)
            certified=bool(real_kl<=FLOOR_B5_RECAL and beats_twin)
            rungrec[name]={"done":True,"params":LAD.get(name,{}).get("params"),
                "SACRED_kl_rep":real_kl,"SACRED_kl_all":sub_s["kl_all"],"SACRED_r2":round(r2_s,4),
                "SACRED_trained_pos_kl":round(kl_sacred_pt,5),"SACRED_behav":sub_s.get("behav"),
                "HOLD2_kl_rep":sub_h["kl_rep"],"HOLD2_r2":round(r2_h,4),
                "WITHIN_kl_rep":round(kl_within,5),"twin_kl_rep":twin_kl,"twin_r2":round(r2_tw,4),
                "beats_twin_2x":beats_twin,"certified":certified,
                "floor":FLOOR_B5_RECAL,"silent_W0":W0}
            res["cert"]["rungs"]=rungrec; write_json()
            logln(f"[cert {name}] SACRED kl_rep={real_kl:.5f} (floor {FLOOR_B5_RECAL}, W0 {W0}, twin {twin_kl:.5f}) "
                  f"r2={r2_s:.4f} within={kl_within:.5f} hold2={sub_h['kl_rep']:.5f} beats_twin={beats_twin} cert={certified}")
            del m,mt; free()
        # pick best rung by SACRED kl_rep
        rr=res["cert"]["rungs"]
        best=min(rr.items(),key=lambda kv:kv[1]["SACRED_kl_rep"])
        best_name,best_rec=best
        best_kl=best_rec["SACRED_kl_rep"]; best_twin=best_rec["twin_kl_rep"]; W0=res["cert"]["gates"]["silent_rep"]
        if best_rec["certified"]:
            bandA="CERTIFIED"
        elif best_kl<=WALL_09 and best_kl<best_twin and best_kl<0.9*W0:
            bandA="PARTIAL"
        else:
            bandA="NULL/INTERACTIONALLY-EMERGENT"
        bh=best_rec.get("SACRED_behav") or {}
        cfr=bh.get("copy_fidelity_ratio",0.0)
        bandBEH=("FAITHFUL" if cfr>=0.9 else ("DEGRADED" if cfr>=0.5 else "BROKEN"))
        res["cert"].update({"done":True,"best_rung":best_name,"best_SACRED_kl_rep":best_kl,
            "H_V6_A":bandA,"bands_A":{"CERTIFIED":"<=0.1279 & <=0.5*twin","PARTIAL":">floor & <=3.11403 & <twin & <0.9*W0",
                                      "NULL":"else"},"bet_A":"PARTIAL 50 / NULL 35 / CERTIFIED 15",
            "H_V6_BEHAV":bandBEH,"copy_fidelity_ratio":cfr,"bet_behav":"DEGRADED 45 / FAITHFUL 35 / BROKEN 20",
            "wall_S4":WALL_S4,"floor":FLOOR_B5_RECAL,"silent_W0":W0})
        write_json()
        logln(f"[CERT] best={best_name} SACRED kl_rep={best_kl:.5f} -> H-V6-A={bandA}; behav ratio={cfr} -> {bandBEH}")

        # FAILURE BRANCH: KL-finetune if best is PARTIAL and <=2*floor
        if bandA=="PARTIAL" and best_kl<=2*FLOOR_B5_RECAL and not res["cert"].get("finetune") and el()<HARD_WALL_S:
            logln("==== FAILURE BRANCH: KL-finetune the best rung ====")
            m=make_rung(best_name,CERT_BLOCK).to('cuda').train()
            m.load_state_dict({k:v.to('cuda') for k,v in BASES[f"sd_{best_name}_real"].items()})
            optf=torch.optim.Adam(m.parameters(),lr=FT_LR)
            fbk=feats_tr_g.reshape(Ntr,CERT_BLOCK,FEAT_DIM); obk=obj_tr_g.reshape(Ntr,CERT_BLOCK,d)
            yc_cache=clean_logits(IDS_TRAIN)   # clean train logits, precomputed once
            fl=[]
            for st in range(FT_STEPS):
                optf.zero_grad(set_to_none=True); loss=0.0
                for ci,s0 in enumerate(range(0,Ntr,MB)):    # per-chunk fwd+bwd (independent graphs)
                    s1=min(Ntr,s0+MB)
                    if best_name=="L2": raw=m(fbk[s0:s1]).reshape(-1,d)
                    else: raw=m(fbk[s0:s1].reshape(-1,FEAT_DIM))
                    oh=proj_compl(raw)
                    objc=obk[s0:s1].reshape(-1,d)
                    delta=(oh-objc).reshape(s1-s0,CERT_BLOCK,d).clone(); delta[:, :IND_SEG, :]=0.0
                    inj5.add=delta; inj5.on=True
                    lg=M["m"](IDS_TRAIN[s0:s1].to('cuda'),use_cache=False).logits; inj5.on=False; inj5.add=None
                    yc=yc_cache[ci].float()
                    logp=Fnn.log_softmax(yc,-1); p=logp.exp(); lp=Fnn.log_softmax(lg.float(),-1)
                    kl=(p*(logp-lp)).sum(-1)[:,IND_SEG:CERT_BLOCK].mean()
                    (kl*(s1-s0)/Ntr).backward(); loss+=float(kl.item())*(s1-s0)/Ntr
                optf.step(); fl.append(loss)
                if (st+1)%max(1,FT_STEPS//10)==0: logln(f"[FT] step {st+1}/{FT_STEPS} trainKL={loss:.5f}")
            m.eval()
            oh_s,obj_s,_=run_surrogate(best_name,m,IDS_SACRED,f"ft-sacred-{best_name}")
            sub_s=substitution_kl(oh_s,obj_s,IDS_SACRED,f"ft-sacred-{best_name}",want_behav=True)
            ft_cert=bool(sub_s["kl_rep"]<=FLOOR_B5_RECAL)
            BASES[f"sd_{best_name}_ft"]={k:v.detach().cpu() for k,v in m.state_dict().items()}; save_bases()
            res["cert"]["finetune"]={"rung":best_name,"train_kl_curve":[round(x,5) for x in fl[::max(1,len(fl)//20)]],
                "SACRED_kl_rep":sub_s["kl_rep"],"certified_via_ft":ft_cert,"behav":sub_s.get("behav")}
            write_json(); logln(f"[FT] SACRED kl_rep={sub_s['kl_rep']:.5f} certified_via_ft={ft_cert}")
            del m; free()
    inj5.close()

    # =================================================================================
    # ARM B -- folded r48-class reads at rep b8..b11 (VERBATIM V5 B2 recipe, parameterized)
    # =================================================================================
    if not res["armB"].get("done") and el()<HARD_WALL_S:
        gpu_free_check("armB")
        logln("==== ARM B: folded r48-class reads at rep b8..b11 ====")
        import numpy as np
        rep_s=build_dind(N_SACRED,CERT_BLOCK,REP_SEED)
        STREAMS_B={"prose":ids_window(WIKI,FRESH_LO,FRESH_HI,"fresh prose")[:N_SACRED],
                   "repetition":rep_s}
        try:
            cids=M["tok"](load_code_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
            STREAMS_B["code"]=ids_window(cids,FRESH_LO,FRESH_HI,"fresh code")[:N_SACRED]
        except Exception as e: logln(f"[armB] code load skipped {e}")
        armb=res["armB"].get("bounds",{})
        for b in ARMB_BOUNDS:
            if armb.get(str(b),{}).get("done"): continue
            if el()>HARD_WALL_S: break
            gram=torch.zeros(d,d,dtype=torch.float64); ntok=0
            B2d=B2_g.double()
            for reg in (["prose","repetition"] if SMOKE else REGIMES):
                if reg not in STREAMS_B: continue
                Hc=capture_h_all(STREAMS_B[reg],CAP_CHUNK,f"armB-{reg}-b{b}",which=[b])
                h=Hc[b].to('cuda').double(); rr=h-mu_all[b].to('cuda').double(); rr=rr-(rr@B2d)@B2d.t()
                gram+=(rr.t()@rr).cpu().double(); ntok+=rr.shape[0]; del h,rr,Hc; free()
            G=gram/max(1,ntok); evals,evecs=torch.linalg.eigh(G); evals=evals.clamp(min=0)
            order=torch.argsort(evals,descending=True); V=evecs[:,order].float().to('cuda')
            Ycr=clean_logits(rep_s); NHr=rep_s.shape[0]
            Hb=capture_h_all(rep_s,CAP_CHUNK,f"armB-repb{b}",which=[b]); Xc=Hb[b].to('cuda')-mu_all[b].to('cuda')
            Ecur_all=wte_g[rep_s.reshape(-1).to('cuda')]
            inj=InjectHook(M["blocks"][b-1])
            kl_idb=inject_kl_full(rep_s,inj,torch.zeros(NHr,CERT_BLOCK,d,device='cuda'),Ycr)
            b2P=(Xc@B2_g)@B2_g.t(); q35P=(Xc@Q35_g)@Q35_g.t()
            yhat=Ecur_all@wteW_g[b].t()+wtec_g[b]; y2=yhat-(yhat@B2_g)@B2_g.t(); y4=y2-(y2@Q35_g)@Q35_g.t()
            curve={}; replay_fail=[]
            for rk in RANKS_ARMB:
                Ok=V[:, :rk]; Op=Ok-span5@(span5.t()@Ok)
                Usvd,Ssvd,_=torch.linalg.svd(Op,full_matrices=False); keep=Ssvd>1e-2; O_r=Usvd[:,keep].contiguous()
                net=int(O_r.shape[1])
                oP=(Xc@O_r)@O_r.t(); yk=y4-(y4@O_r)@O_r.t()
                kl=inject_kl_full(rep_s,inj,(b2P+q35P+oP+yk-Xc).reshape(NHr,CERT_BLOCK,d),Ycr)
                bank=V3_S7.get(f"repetition_b{b}") if rk==20 else None
                ok=(abs(kl-bank)<=3e-3) if (bank is not None and not SMOKE) else True
                if not ok: replay_fail.append({"b":b,"rank":rk,"kl":kl,"banked":bank})
                curve[str(rk)]={"net_dims":net,"KL":round(kl,5),"replay_ok":bool(ok),"total_unnamed_folded":14+net}
                if rk==48: BASES[f"O_r48_b{b}"]=O_r.cpu().contiguous(); save_bases()
                logln(f"[armB b{b} r{rk}] net={net} KL={kl:.5f} (S7 bank {bank}) ok={ok}")
            inj.close()
            if replay_fail: res["instrument_discrepancy"].append({"stage":"armB-replay","name":f"b{b}","why":replay_fail})
            kl48=curve.get("48",{}).get("KL"); fl_rec=floors_rec[b]["repetition"]; fl_leg=floors_leg[b]["repetition"]
            closes=bool(kl48 is not None and fl_rec is not None and kl48<=fl_rec and kl_idb==0.0 and RECAL_OK)
            armb[str(b)]={"done":True,"identity_kl":kl_idb,"curve":curve,"KL_r48":kl48,
                "floor_recal":fl_rec,"floor_legacy":fl_leg,
                "H_V6_B":("CLOSES-RECAL" if closes else "STAYS"),
                "legacy_leg":{"KL":kl48,"floor":fl_leg,"pass":bool(kl48 is not None and kl48<=fl_leg)}}
            res["armB"]["bounds"]=armb; write_json()
            logln(f"[armB b{b}] r48={kl48} vs recal {fl_rec} legacy {fl_leg} -> {armb[str(b)]['H_V6_B']}")
            del Ycr,Hb,Ecur_all,V,G,evecs,evals; free()
        res["armB"]["done"]=True; write_json()

    # =================================================================================
    # ARM C (stretch) -- code-column recon probe at code_b7
    # =================================================================================
    if not res["armC"].get("done"):
        if el()<ARM_C_GATE_S and el()<HARD_WALL_S and not SMOKE:
            gpu_free_check("armC")
            logln("==== ARM C: code-column recon probe (code_b7) ====")
            try:
                b=ARMC_CODE_B
                cids=M["tok"](load_code_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
                code_s=ids_window(cids,FRESH_LO,FRESH_HI,"fresh code")[:N_SACRED]
                Ycr=clean_logits(code_s); NHc=code_s.shape[0]
                Hb=capture_h_all(code_s,CAP_CHUNK,f"armC-codeb{b}",which=[b]); Xc=Hb[b].to('cuda')-mu_all[b].to('cuda')
                Ecur_all=wte_g[code_s.reshape(-1).to('cuda')]
                inj=InjectHook(M["blocks"][b-1])
                kl_id=inject_kl_full(code_s,inj,torch.zeros(NHc,CERT_BLOCK,d,device='cuda'),Ycr)
                b2P=(Xc@B2_g)@B2_g.t(); q35P=(Xc@Q35_g)@Q35_g.t()
                # candidate reads of the code object; delta = (keep span5 + objread) - Xc:
                def kl_read(objread):
                    delta=(b2P+q35P+objread-Xc).reshape(NHc,CERT_BLOCK,d)
                    return inject_kl_full(code_s,inj,delta,Ycr)
                # (a) silent: objread=0
                kl_silent=kl_read(torch.zeros_like(Xc))
                # (b) wte-term
                yhat=Ecur_all@wteW_g[b].t()+wtec_g[b]; y2=yhat-(yhat@B2_g)@B2_g.t(); y4=y2-(y2@Q35_g)@Q35_g.t()
                kl_wte=kl_read(y4)
                # (c) W_U-informed: project object onto top unembedding-aligned directions of the residual
                WU=M["m"].lm_head.weight.detach().float()  # (vocab,768)
                # top-64 right singular dirs of W_U as the "readout" subspace
                _,_,VhU=torch.linalg.svd(WU,full_matrices=False); Uwu=VhU[:64].t().contiguous()
                Uwu=Uwu-span5@(span5.t()@Uwu); Uwu,_=torch.linalg.qr(Uwu)
                objWU=(Xc@Uwu)@Uwu.t(); kl_WU=kl_read(objWU + (y4-(y4@Uwu)@Uwu.t()))
                # (d) intermediate low-rank oracle r48 (does rank close it, like b12?)
                gram=torch.zeros(d,d,dtype=torch.float64); B2d=B2_g.double()
                h=Hb[b].to('cuda').double(); rr=h-mu_all[b].to('cuda').double(); rr=rr-(rr@B2d)@B2d.t()
                gram=(rr.t()@rr).cpu().double()/rr.shape[0]
                evals,evecs=torch.linalg.eigh(gram); order=torch.argsort(evals.clamp(min=0),descending=True); V=evecs[:,order].float().to('cuda')
                Ok=V[:, :48]; Op=Ok-span5@(span5.t()@Ok); Us,Ss,_=torch.linalg.svd(Op,full_matrices=False); O_r=Us[:,Ss>1e-2].contiguous()
                oP=(Xc@O_r)@O_r.t(); kl_r48=kl_read(oP + (y4-(y4@O_r)@O_r.t()))
                inj.close()
                res["armC"]={"done":True,"boundary":f"code_b{b}","identity_kl":kl_id,
                    "S7_bank":V3_S7.get(f"code_b{b}"),"floor_recal":floors_rec[b]["code"],
                    "kl_silent":round(kl_silent,5),"kl_wte_term":round(kl_wte,5),
                    "kl_WU_read":round(kl_WU,5),"kl_r48_oracle":round(kl_r48,5),
                    "interpretation":"lowest KL among {wte,WU,r48} names the dominant late-code content class",
                    "note":"recon for V7, not closure; report-only, no band"}
                write_json(); logln(f"[armC] silent={kl_silent:.4f} wte={kl_wte:.4f} WU={kl_WU:.4f} r48={kl_r48:.4f}")
                del Ycr,Hb,Xc,Ecur_all; free()
            except Exception as ce:
                res["armC"]={"done":True,"error":str(ce),"trace":traceback.format_exc()[:1500]}
                logln(f"[armC] ERROR {ce}"); write_json()
        else:
            res["armC"]={"done":True,"skipped":True,"reason":"wall-bound or smoke (pre-registered drop)"}
            write_json(); logln("[armC] DROPPED (gate)")

    # =================================================================================
    # VERDICT -- H-OPEN6-a VERBATIM, BOTH METERS (recal primary), V6 grain overrides
    # =================================================================================
    if not SMOKE and not res["verdict"].get("done"):
        v3=json.load(open(os.path.join(DIR,"_v3_result.json"),encoding="utf-8"))
        cells=v3["cells"]; allcells=[(r,b) for r in REGIMES for b in range(nL+1)]
        certA=bool(res["cert"].get("H_V6_A")=="CERTIFIED")
        best_name=res["cert"].get("best_rung"); best_kl=res["cert"].get("best_SACRED_kl_rep")
        armb_b=res["armB"].get("bounds",{})
        def armb_close(b):
            rec=armb_b.get(str(b),{})
            return (rec.get("H_V6_B")=="CLOSES-RECAL", rec.get("KL_r48"))
        def vgrain(key,meter):
            cell=cells[key]; kl=cell["KL"]["S7"]; grain="S7"
            if key=="repetition_b5" and certA and best_kl is not None:
                kl=best_kl; grain=f"S9x-surrogate({best_name})"
            if key=="repetition_b12":
                kl=B12_R48_BANK; grain="S7-r48-folded(carried V5)"
            for bb in (8,9,10,11):
                if key==f"repetition_b{bb}":
                    cl,k48=armb_close(bb)
                    if cl and k48 is not None: kl=k48; grain="S7-r48-folded"
            return kl,grain
        tables={}
        for meter in ("legacy","recal"):
            tab={}; N_open=0; N_grain=0; gaps=[]
            for (r,b) in allcells:
                key=f"{r}_b{b}"; cell=cells[key]
                if meter=="legacy": fl=floors_leg[b][r]
                else:
                    fl=floors_rec[b].get(r) if r!="prose" else 0.1871
                    if fl is None or not RECAL_OK: fl=floors_leg[b][r]
                kl,grain=vgrain(key,meter)
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
        res["verdict"]={"done":True,"H_V6_VERDICT":Ha,"primary_meter":primary,"tables":tables,
            "surrogate_certified":certA,"best_rung":best_name,"best_SACRED_kl_rep":best_kl,
            "armb_closures":{str(b):armb_close(b)[0] for b in (8,9,10,11)},
            "verdict_bet":"NOT-YET 80 / OPEN-AT-GRAIN 15 / OPEN 5","g_room":0.8614,
            "escalation":("NOT-YET -> gap tables (both meters) + STOP, Will decides" if Ha=="NOT-YET"
                          else "band MET -> program-complete recommendation + STOP")}
        write_json()
        logln(f"[VERDICT] primary={primary} H-V6={Ha} | recal N_grain={tables['recal']['N_grain']} "
              f"gaps={tables['recal']['gap_cells']} unexpl={tables['recal']['unexplained_nats']} | "
              f"legacy N_grain={tables['legacy']['N_grain']} gaps={tables['legacy']['gap_cells']} "
              f"unexpl={tables['legacy']['unexplained_nats']}")

    # ---- freeze decoder_v6 IFF certified (pre-reg clause) ----
    if not SMOKE and res["cert"].get("H_V6_A")=="CERTIFIED" and not res.get("v6_frozen"):
        best_name=res["cert"]["best_rung"]
        v3T=torch.load(os.path.join(DIR,"decoder_v3_tensors.pt"),map_location="cpu",weights_only=False)
        v6T=dict(v3T)
        v6T["surrogate_rung"]=best_name; v6T["surrogate_state_dict"]=BASES[f"sd_{best_name}_real"]
        v6T["surrogate_scaler_mean"]=BASES["sc_mean"]; v6T["surrogate_scaler_std"]=BASES["sc_std"]
        v6T["m0_repera_Vk_recal"]=Vk.cpu()
        for b in (8,9,10,11):
            if f"O_r48_b{b}" in BASES: v6T[f"O_r48_b{b}"]=BASES[f"O_r48_b{b}"]
        tmp=os.path.join(DIR,"decoder_v6_tensors.pt.tmp"); torch.save(v6T,tmp); os.replace(tmp,os.path.join(DIR,"decoder_v6_tensors.pt"))
        cfg={"version":"DECODER_V6 1.0 (2026-07-05)","propose_only":True,"pre_registration":PEN,
             "assembly":"V3 + S9x executable surrogate rung at rep-b5 (certified on held-out periods) + Arm-B folded reads",
             "surrogate":{"rung":best_name,"SACRED_kl_rep":res["cert"]["best_SACRED_kl_rep"],
                          "floor":FLOOR_B5_RECAL,"input_contract":"[L2 state, current-token wte, m0 k*=1 coeff]"},
             "source_sha256":O["src_sha"]}
        tmp=os.path.join(DIR,"decoder_v6.json.tmp")
        with open(tmp,"w",encoding="utf-8") as f: json.dump(cfg,f,indent=1,default=str)
        os.replace(tmp,os.path.join(DIR,"decoder_v6.json"))
        res["v6_frozen"]={"tensors_sha":sha256(os.path.join(DIR,"decoder_v6_tensors.pt")),
                          "json_sha":sha256(os.path.join(DIR,"decoder_v6.json"))}
        write_json(); logln(f"[FREEZE] DECODER_V6 frozen: {res['v6_frozen']}")

    # ================= SMOKE / STATUS =================
    if SMOKE:
        sm={"M0a":res["gates"]["M0a"]["pass"],"data":bool(res["data"].get("done")),
            "ladder":all(res["ladder"].get(n,{}).get("done") for n in RUNGS),
            "cert":bool(res["cert"].get("done")),"armB":bool(res["armB"].get("done")),
            "cert_gates_id":res.get("cert",{}).get("gates",{}).get("identity_kl")}
        ok=all(bool(v) for k,v in sm.items() if k!="cert_gates_id") and (res.get("cert",{}).get("gates",{}).get("identity_kl")==0.0)
        res["S_smoke"]=sm; res["status"]="SMOKE-"+("OK" if ok else "FAIL")
        logln(f"[SMOKE] {json.dumps(sm)} -> {res['status']}")
    else:
        done=(bool(res["data"].get("done")) and bool(res["cert"].get("done"))
              and bool(res["armB"].get("done")) and bool(res["armC"].get("done")) and bool(res["verdict"].get("done")))
        res["status"]=("COMPLETE" if (done and not res["instrument_discrepancy"]) else
                       ("COMPLETE-WITH-DISCREPANCY" if done else "PARTIAL"))
    save_bases(); write_json()
    if M["m"] is not None: del M["m"]; M["m"]=None; free()
except Exception as e:
    res["fatal_error"]={"error":str(e),"trace":traceback.format_exc()}
    logln(f"FATAL {e}\n{traceback.format_exc()}"); res.setdefault("status","FATAL")
write_json()
logln(f"V6 END status={res.get('status')} elapsed={el()}s")
open(os.path.join(DIR,"_v6_smoke_gpu.done" if SMOKE else "_v6_gpu.done"),"w").write(str(res.get("status","?"))+"\n")
logln("*** V6_"+("SMOKE_" if SMOKE else "")+"DONE ***"); LOG.flush(); LOG.close(); print("done")
