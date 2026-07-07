# _l1.py -- L1 NAMES AT SCALE (Babel chain Stage 1). GPT-2 124M. PROPOSE-ONLY.
# Pre-registration: FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md ::
#   "L1 -- NAMES AT SCALE (BABEL STAGE 1) ... GAP-SCAN + PRE-REGISTRATION (2026-07-05 ~23:52)".
# Instrument: the V4/V4C Arm-C snap battery VERBATIM as actuator (SnapHook on all 12 attn writes,
#   fac=(a0+s*m*sigma)/a0 at top-16 |traffic| positions), EXTENDED readouts per pre-reg:
#   CH-WU (final W_U class contrast) + CH-INT (logit-lens contrast at b+1..b+3) + CH-FIELD (V4
#   downstream-field antisymmetry) as verdict channels, CH-POS report-only; 3 regime banks
#   (prose/code/repetition); sigma-matched nulls (B_NULL=20, seeds 9000+jseed*100+it) on EVERY
#   verdict channel. Gates G0-G5 verdict-blocking. Per-word atomic checkpoint + resume-skip.
import json, time, os, math, gc, subprocess, ctypes, hashlib
import torch
import torch.nn.functional as Fnn

t0=time.time()
DIR=r"C:\Shadow\Dissector\D0_PROGRAM\CONSTRUCTIVE"
SMOKE=os.environ.get("L1_SMOKE")=="1"
LOG=open(os.path.join(DIR,"_l1.log"),"a",encoding="utf-8")
def logln(s):
    s=str(s); LOG.write(f"[L1 {round(time.time()-t0,1):8.1f}s] "+s+"\n"); LOG.flush()
    try: print(s,flush=True)
    except Exception: pass
def el(): return round(time.time()-t0,1)
logln("="*100); logln(f"L1 START smoke={SMOKE} torch={torch.__version__}")
try:
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(),0x4000)
    logln("[ops] priority BelowNormal set")
except Exception as e: logln(f"[ops] priority set failed: {e}")
torch.set_num_threads(6)

# ---------------- locked constants (pre-reg verbatim) ----------------
CERT_BLOCK=512; IND_SEG=64; MB=4; CAP_CHUNK=16; A_EPS=1e-6
VOCAB_SANS_SPECIALS=50256; REGIMES=["prose","code","repetition"]
FRESH_LO,FRESH_HI=24576,32768; REP_SEED=3
B_NULL=3 if SMOKE else 20; B_NULL_FAST=12
ROOMS=[2,5,3,4,6]
W_CORR_J=[0,1] if SMOKE else [0,1,2,3,4,6,9,10,12,15,17,20,26,29,34]
FOLD_CELLS=([("code",9,"O_r48_code_b9","v7")] if SMOKE else
    [("repetition",8,"O_r48_b8","v7t"),("repetition",9,"O_r48_b9","v7t"),
     ("repetition",10,"O_r48_b10","v7t"),("repetition",11,"O_r48_b11","v7t"),
     ("repetition",12,"O_r48_b12","v5"),
     ("code",4,"O_r48_code_b4","v7t"),("code",5,"O_r48_code_b5","v7t"),
     ("code",6,"O_r48_code_b6","v7t"),("code",7,"O_r48_code_b7","v7t"),
     ("code",8,"O_r48_code_b8","v7t"),("code",9,"O_r48_code_b9","v7t"),
     ("code",10,"O_r48_code_b10","v7t"),("code",11,"O_r48_code_b11","v7t"),
     ("prose",12,"O_r48_prose_b12","v7t")])
SHARE_MIN=0.01; DEDUP_DOT=0.8
SMOKE_FOLD_CAP=2       # smoke only: top-2 candidates of the single smoke cell
C_BANKED={0:{"C":-0.6281,"beats":True},16:{"C":-1.5931,"beats":True}}
DEC_V7_SHA="b1d2f464c00c3ef6"; V5B_SHA="04c401d24ab2cd9d"
CODE_B9_BANK=0.13721; TOL_REPLAY=2e-3; TOL_ANCHOR=3e-3
N_STAND_ANCHOR=64; N_BANK=16
SOFT_COMPUTE_S=3.5*3600; HARD_WALL_S=4.5*3600
RESULT_JSON=os.path.join(DIR,"_l1_result_SMOKE.json" if SMOKE else "_l1_result.json")
BASES_PT=os.path.join(DIR,"_l1_bases_SMOKE.pt" if SMOKE else "_l1_bases.pt")
torch.manual_seed(1234)

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for ch in iter(lambda:f.read(1<<20),b""): h.update(ch)
    return h.hexdigest()[:16]

PEN=("FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md :: 'L1 -- NAMES AT SCALE (BABEL STAGE 1) -- "
     "GAP-SCAN + PRE-REGISTRATION (2026-07-05 ~23:52)'")
res={"experiment":"L1 NAMES AT SCALE: V4C snap battery extended (CH-WU/CH-INT/CH-FIELD verdict "
     "channels + CH-POS report-only) x 3 regimes x sigma-matched nulls, over the 15 W-CORR words "
     "(14 V4C-unnamed + glitch b2_d0) + all deduped >=1%-share folded-read dims from decoder_v7 "
     "provenance. NAMED / NAMED-REGIME-SPECIFIC / CERTIFIED-NO-GLOSS per locked rubric.",
     "date":"2026-07-05","propose_only":True,"pre_registration":PEN,"smoke":SMOKE,
     "config":{"b_null":B_NULL,"precision":"fp32","tf32":"off","attn":"eager","seed":1234,
               "null_seeds":"9000+jseed*100+it; jseed=corridor j (W-CORR) / 100+i (W-FOLD)",
               "snap":"sigma-matched (null fac uses the REAL word's sigma; _v4.py:1189 verbatim)",
               "share_min":SHARE_MIN,"dedup_dot":DEDUP_DOT},
     "gpu_free_checks":[],"instrument_discrepancy":[],"gates":{},"mass":{},"wordlist":{},
     "words":{},"budget":{},"verdict":{},"status":"INIT"}
def write_json():
    res["elapsed_s"]=el(); tmp=RESULT_JSON+".tmp"
    with open(tmp,"w",encoding="utf-8") as f: json.dump(res,f,indent=1,default=str)
    os.replace(tmp,RESULT_JSON)
BASES={}
def save_bases():
    tmp=BASES_PT+".tmp"; torch.save(BASES,tmp); os.replace(tmp,BASES_PT)

# resume
if os.path.exists(RESULT_JSON):
    try:
        prev=json.load(open(RESULT_JSON,encoding="utf-8"))
        for k in ("gates","mass","wordlist","words","budget","gpu_free_checks","instrument_discrepancy"):
            if prev.get(k): res[k]=prev[k]
        logln(f"*** RESUME *** prior words done={sum(1 for w in res['words'].values() if w.get('done'))}")
    except Exception as e: logln(f"resume load fail {e}")
if os.path.exists(BASES_PT):
    try: BASES=torch.load(BASES_PT,map_location="cpu",weights_only=False)
    except Exception as e: logln(f"bases resume fail {e}")
write_json()

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
    rec["clear"]=not rec["foreign"]
    if rec["foreign"]: res["instrument_discrepancy"].append({"stage":tag,"name":"gpu_free_check","why":str(rec["foreign"])})
    res["gpu_free_checks"].append(rec); write_json(); logln(f"[gpu {tag}] clear={rec['clear']}"); return rec["clear"]
def free(): gc.collect(); torch.cuda.empty_cache()

# ---------------- model (verbatim loader) ----------------
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
def ids_window(all_ids,lo,hi,what):
    if len(all_ids)<hi: raise RuntimeError(f"{what}: {len(all_ids)}<{hi}")
    n=(hi-lo)//CERT_BLOCK; return torch.tensor(all_ids[lo:hi],dtype=torch.long).view(n,CERT_BLOCK)

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
    logln(f"[capture {tag}] boundaries={sorted(which)} shape={tuple(H[which[0]].shape)} chunk={chunk}")
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
def inject_kl_full(ids_cpu,injhook,delta_full_g,Yclean):
    model=M["m"]; N=ids_cpu.shape[0]; tot=0.0; cnt=0; ci=0
    with torch.no_grad():
        for s0 in range(0,N,MB):
            s1=min(N,s0+MB)
            injhook.add=delta_full_g[s0:s1]; injhook.on=True
            lg=model(ids_cpu[s0:s1].to('cuda'),use_cache=False).logits; injhook.on=False; injhook.add=None
            kl=fkl(Yclean[ci].float(),lg.float()); tot+=kl.sum().item(); cnt+=kl.numel(); ci+=1
            del lg
    return tot/max(1,cnt)

def pct95(xs):
    xs=sorted(xs); return xs[min(len(xs)-1,int(math.ceil(0.95*len(xs))-1))] if xs else 0.0

# ---------------- SnapHook + class/capture readout (V4 verbatim) ----------------
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
    # G3: fac=ones with P=I must reproduce the hookless forward at matched chunking (MB)
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

# ======================================================================================
# MAIN
# ======================================================================================
try:
    gpu_free_check("l1-start")
    ensure_model()
    d=M["d"]; nL=M["nL"]; tok=M["tok"]
    wte_g=M["wte"].detach().float()
    lnf_w=M["m"].transformer.ln_f.weight.detach().float()

    # ---------- G1: M0a-subset content gate (V4C verbatim) ----------
    o1=torch.load(os.path.join(DIR,"_open1_bases.pt"),map_location="cpu",weights_only=False)
    mu=o1["mu"].float(); B2=o1["B2"].float(); U=o1["U"]
    v1=torch.load(os.path.join(DIR,"decoder_v1_tensors.pt"),map_location="cpu",weights_only=False)
    def md(a,b): return float((a.float()-b.float()).abs().max())
    cm={"B2_vs_v1":md(B2,v1["B2"].float()),"mu_vs_v1":md(mu,v1["mu"].float())}
    p4=json.load(open(os.path.join(DIR,"_open4_probe.json"),encoding="utf-8"))
    frozen=[(r["room"],r["dim"]) for r in p4["selection"]["corridor_distinct"]]
    seen=[]; kept=[]
    for b in ROOMS:
        for i in range(16):
            u=U[b][:,i].float(); best=0.0
            for (kb,ki,v) in seen:
                dd=abs(float(u@v))
                if dd>best: best=dd
            if best<=0.8: kept.append((b,i))
            seen.append((b,i,u))
    corr_match=bool(kept==frozen)
    V35=torch.stack([U[r][:,d_].float() for (r,d_) in frozen],1)
    g1_ok=(all(v==0.0 for v in cm.values()) and corr_match and len(frozen)==35)
    res["gates"]["G1_M0a_subset"]={"content_match":cm,"corridor_recompute_match":corr_match,
                                   "n_corridor":len(frozen),"pass":bool(g1_ok)}
    logln(f"[G1] cm={cm} corr_match={corr_match} -> {'PASS' if g1_ok else 'FAIL'}"); write_json()
    if not g1_ok: raise RuntimeError("G1 M0a-subset FAILED -- clean kill")

    # ---------- G2: fold provenance ----------
    sha7=sha256(os.path.join(DIR,"decoder_v7_tensors.pt")); sha5=sha256(os.path.join(DIR,"_v5_bases.pt"))
    dv7=torch.load(os.path.join(DIR,"decoder_v7_tensors.pt"),map_location="cpu",weights_only=False)
    v5b=torch.load(os.path.join(DIR,"_v5_bases.pt"),map_location="cpu",weights_only=False)
    Q35=dv7["Q35"].float()
    span5=torch.cat([B2,Q35],1)
    OB={}
    orth_worst=0.0; span_worst=0.0
    for (reg,b,key,src) in FOLD_CELLS:
        O=(v5b[key] if src=="v5" else dv7[key]).float()
        orth_worst=max(orth_worst,float((O.t()@O-torch.eye(O.shape[1])).norm()))
        span_worst=max(span_worst,float((span5.t()@O).abs().max()))
        OB[key]=O
    g2_ok=bool(sha7==DEC_V7_SHA and sha5==V5B_SHA and orth_worst<=1e-3 and span_worst<=1e-3)
    res["gates"]["G2_fold_provenance"]={"dec_v7_sha":sha7,"v5_bases_sha":sha5,"orth_worst":orth_worst,
                                        "span5_dot_worst":span_worst,"pass":g2_ok}
    logln(f"[G2] sha7={sha7} sha5={sha5} orth={orth_worst:.2e} span={span_worst:.2e} -> {'PASS' if g2_ok else 'FAIL'}")
    write_json()
    if not g2_ok: raise RuntimeError("G2 fold provenance FAILED -- clean kill")

    # ---------- streams ----------
    wt=torch.load(os.path.join(DIR,"_t14_wt103_ids.pt"),map_location="cpu",weights_only=False)
    stand64=ids_window(wt["ids"].tolist(),wt["lo"],wt["lo"]+N_STAND_ANCHOR*CERT_BLOCK,"wt103 standing")[:N_STAND_ANCHOR]
    STREAMS={"prose":stand64[:N_BANK],
             "repetition":build_dind(N_BANK,CERT_BLOCK,REP_SEED)}
    CIDS=tok(load_code_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
    STREAMS["code"]=ids_window(CIDS,FRESH_LO,FRESH_HI,"fresh code")[:N_BANK]
    WIKI2=tok(load_wiki_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
    MASS_PROSE=ids_window(WIKI2,FRESH_LO,FRESH_HI,"fresh prose")[:N_BANK]

    # ---------- captures ----------
    fold_bounds=sorted({b for (_,b,_,_) in FOLD_CELLS})
    corr_bounds=sorted({frozen[j][0] for j in W_CORR_J})
    bat_bounds=sorted(set(corr_bounds)|set(fold_bounds))
    CAPS={reg:capture_h_all(STREAMS[reg],CAP_CHUNK,f"bank-{reg}",which=bat_bounds) for reg in REGIMES}
    mass_pb=sorted({b for (reg,b,_,_) in FOLD_CELLS if reg=="prose"})
    CAP_MASS_PROSE=capture_h_all(MASS_PROSE,CAP_CHUNK,"mass-prose",which=mass_pb) if mass_pb else {}

    # ---------- G3: snap identity at matched batch shape ----------
    g3={}
    for reg in REGIMES:
        g3[reg]=snap_identity_check(STREAMS[reg][:4].to('cuda'))
    g3_ok=all(v<=1e-4 for v in g3.values())
    res["gates"]["G3_snap_identity"]={"max_dlogit":g3,"pass":bool(g3_ok)}
    logln(f"[G3] {g3} -> {'PASS' if g3_ok else 'FAIL'}"); write_json()
    if not g3_ok: raise RuntimeError("G3 snap identity FAILED -- clean kill")

    B2_g=B2.to('cuda'); Q35_g=Q35.to('cuda'); span5_g=span5.to('cuda'); mu_all=mu
    V35_g=V35.to('cuda'); Pfull=torch.eye(d,device='cuda')

    # ---------- battery core (V4 armC machinery; extended readouts) ----------
    wte_cpu=wte_g.cpu(); lnf_cpu=lnf_w.cpu(); lnf_gpu=lnf_w.to('cuda')
    def word_battery(vdir_g,bnd,regime,jseed,bnull,null_orth_q35,tag):
        """Runs the full extended battery for one word in one regime. Returns record dict."""
        H=CAPS[regime][bnd].to('cuda'); ids_full=STREAMS[regime].to('cuda')
        a=(H-mu_all[bnd].to('cuda'))@vdir_g; sigma=float(a.std())
        col=wte_g@(vdir_g*lnf_gpu); top=torch.topk(col,40).indices; bot=torch.topk(-col,40).indices
        class_idx=[top,bot]
        Wtop=wte_cpu[top.cpu()]; Wbot=wte_cpu[bot.cpu()]
        int_blocks=[x for x in (bnd,bnd+1,bnd+2) if x<=nL-1]     # boundaries bnd+1..bnd+3
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
            for si,s in enumerate([1.0,-1.0]):
                fac=torch.ones(nP,CERT_BLOCK,device='cuda')
                for r,t in enumerate(flatidx):
                    a0=float(a[t]); pos=t%CERT_BLOCK
                    if abs(a0)>=A_EPS: fac[r,pos]=(a0+s*mag*sigma)/a0
                mod_,capm=measure_class_snap_cap(M["m"],snap,ids_b,Pfull,ci,fac,class_idx,MB,capb)
                dvs=[]; intd={k:[] for k in int_blocks}
                for r,t in enumerate(flatidx):
                    pos=t%CERT_BLOCK; delt[r,si]=mod_[r,pos]-base[r,pos]
                    if has_field:
                        d_lo=capm[bnd-1].reshape(nP,CERT_BLOCK,d)[r,pos]-cap0[bnd-1].reshape(nP,CERT_BLOCK,d)[r,pos]
                        d_hi=capm[bnd].reshape(nP,CERT_BLOCK,d)[r,pos]-cap0[bnd].reshape(nP,CERT_BLOCK,d)[r,pos]
                        dc=(d_hi-d_lo); dc=dc-(dc@vcpu)*vcpu; dvs.append(dc)
                    for k in int_blocks:
                        dk=capm[k].reshape(nP,CERT_BLOCK,d)[r,pos]-cap0[k].reshape(nP,CERT_BLOCK,d)[r,pos]
                        intd[k].append(dk)
                if has_field: Dvec[si]=torch.stack(dvs,0)@B2
                for k in int_blocks: INTd[k][si]=torch.stack(intd[k],0)
            dT=(delt[:,0,0]-delt[:,1,0])/2.0; dB=(delt[:,0,1]-delt[:,1,1])/2.0
            cp=(dT-dB); C=float(cp.mean()); SE=float(cp.std(unbiased=True)/math.sqrt(nP))
            fld=None
            if has_field:
                Dp=Dvec[0].mean(0); Dm=Dvec[1].mean(0)
                fld={"cos":float((Dp@Dm)/max(1e-12,float(Dp.norm())*float(Dm.norm()))),
                     "Dmag":float((Dp-Dm).norm()/2.0),
                     "Dp":Dp,"Dm":Dm}
            ints={}
            for k in int_blocks:
                dk=(INTd[k][0]-INTd[k][1])/2.0                      # (nP, d) antisymmetrized state delta
                dkl=dk*lnf_cpu                                       # logit-lens restricted to class cols
                ct=(dkl@Wtop.t()).mean(-1)-(dkl@Wbot.t()).mean(-1)
                ints[k+1]={"C":float(ct.mean()),"SE":float(ct.std(unbiased=True)/math.sqrt(nP))}
            return {"C":C,"SE":SE,"field":fld,"int":ints}
        r1=push(1.0); r2=push(2.0)
        # sigma-matched nulls
        null_C=[]; null_D=[]; null_INT=[]
        for it in range(bnull):
            Rr=torch.randn(d,generator=torch.Generator().manual_seed(9000+jseed*100+it)).to('cuda')
            Rr=Rr-B2_g@(B2_g.t()@Rr)
            if null_orth_q35: Rr=Rr-Q35_g@(Q35_g.t()@Rr)
            Rr=Rr/Rr.norm().clamp(min=1e-9)
            colr=wte_g@(Rr*lnf_gpu); topr=torch.topk(colr,40).indices; botr=torch.topk(-colr,40).indices
            Wtopr=wte_cpu[topr.cpu()]; Wbotr=wte_cpu[botr.cpu()]
            ar=(H-mu_all[bnd].to('cuda'))@Rr
            fi=torch.topk(ar.abs(),16).indices.tolist(); sq=[t//CERT_BLOCK for t in fi]
            rowsn=torch.tensor(sq,dtype=torch.long,device='cuda'); ids_n=ids_full[rowsn]
            cir=Rr.contiguous(); rcpu=Rr.cpu()
            onesn=torch.ones(len(fi),CERT_BLOCK,device='cuda')
            basen,cap0n=measure_class_snap_cap(M["m"],snap,ids_n,Pfull,cir,onesn,[topr,botr],MB,capb)
            dl=torch.zeros(len(fi),2,2); Dv={}; INTn={k:{} for k in int_blocks}
            for si,s in enumerate([1.0,-1.0]):
                fac=torch.ones(len(fi),CERT_BLOCK,device='cuda')
                for r,t in enumerate(fi):
                    a0=float(ar[t]); pos=t%CERT_BLOCK
                    # SIGMA-MATCHED: snap magnitude = the REAL word's sigma (V4 verbatim)
                    if abs(a0)>=A_EPS: fac[r,pos]=(a0+s*sigma)/a0
                mod_,capm=measure_class_snap_cap(M["m"],snap,ids_n,Pfull,cir,fac,[topr,botr],MB,capb)
                dvs=[]; intd={k:[] for k in int_blocks}
                for r,t in enumerate(fi):
                    pos=t%CERT_BLOCK; dl[r,si]=mod_[r,pos]-basen[r,pos]
                    if has_field:
                        d_lo=capm[bnd-1].reshape(len(fi),CERT_BLOCK,d)[r,pos]-cap0n[bnd-1].reshape(len(fi),CERT_BLOCK,d)[r,pos]
                        d_hi=capm[bnd].reshape(len(fi),CERT_BLOCK,d)[r,pos]-cap0n[bnd].reshape(len(fi),CERT_BLOCK,d)[r,pos]
                        dc=(d_hi-d_lo); dc=dc-(dc@rcpu)*rcpu; dvs.append(dc)
                    for k in int_blocks:
                        dk=capm[k].reshape(len(fi),CERT_BLOCK,d)[r,pos]-cap0n[k].reshape(len(fi),CERT_BLOCK,d)[r,pos]
                        intd[k].append(dk)
                if has_field: Dv[si]=torch.stack(dvs,0)@B2
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
        # channel clears + stability (rubric verbatim)
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
        # CH-POS descriptors (report-only)
        posh=[int(t%CERT_BLOCK) for t in flatidx]
        top64=torch.topk(a.abs(),64).indices
        phase=[int(t%IND_SEG) for t in top64.tolist()] if regime=="repetition" else None
        wte_side=(wte_cpu@vcpu)
        wtop=[tok.decode([i]) for i in torch.topk(wte_side,10).indices.tolist()]
        wbot=[tok.decode([i]) for i in torch.topk(-wte_side,10).indices.tolist()]
        cur=[tok.decode([int(ids_full[t//CERT_BLOCK,t%CERT_BLOCK])]) for t in flatidx[:8]]
        wu_top=[tok.decode([i]) for i in top[:10].tolist()]
        wu_bot=[tok.decode([i]) for i in bot[:10].tolist()]
        rec={"sigma":round(sigma,4),"n_null":bnull,
             "C1":round(r1["C"],4),"SE1":round(r1["SE"],4),"C2":round(r2["C"],4),"SE2":round(r2["SE"],4),
             "dose_ratio":(round(r2["C"]/r1["C"],3) if abs(r1["C"])>1e-9 else None),
             "null95_C":round(null95C,4),"wu_clear":wu_clear,"wu_stable":wu_stable,
             "int1":{str(k):{"C":round(v["C"],4),"SE":round(v["SE"],4)} for k,v in r1["int"].items()},
             "int2":{str(k):{"C":round(v["C"],4),"SE":round(v["SE"],4)} for k,v in r2["int"].items()},
             "int_kstar":(int(kstar) if kstar is not None else None),"maxint1":round(mxi1,4),
             "null95_INT":(round(null95I,4) if null95I is not None else None),
             "int_clear":int_clear,"int_stable":int_stable,
             "field":({"cos1":round(r1["field"]["cos"],4),"cos2":round(r2["field"]["cos"],4),
                       "Dmag1":round(r1["field"]["Dmag"],4),"Dmag2":round(r2["field"]["Dmag"],4),
                       "null95_D":(round(null95D,4) if null95D is not None else None)}
                      if r1["field"] is not None else None),
             "field_clear":field_clear,"field_stable":field_stable,
             "stable":stable,"n_channels_clear":n_clear,
             "pos":{"pos16":posh,"phase64":phase,"wte_top":wtop,"wte_bot":wbot,
                    "cur_tokens":cur,"wu_top":wu_top,"wu_bot":wu_bot}}
        if r1["field"] is not None:
            BASES[f"D_{tag}_{regime}"]=torch.stack([r1["field"]["Dp"],r1["field"]["Dm"]],0)
        del H
        return rec

    # ---------- G4: corridor anchor replay (M-C-REPLAY; V4C stream verbatim) ----------
    if not res["gates"].get("G4_anchor_replay",{}).get("pass"):
        gpu_free_check("G4")
        anch_bounds=sorted({frozen[j][0] for j in ([0] if SMOKE else [0,16])})
        Hs64=capture_h_all(stand64,CAP_CHUNK,"anchor-stand64",which=anch_bounds)
        idg64=stand64.to('cuda')
        g4recs={}; g4_ok=True
        for j in ([0] if SMOKE else [0,16]):
            rm,dm=frozen[j]; vdir=V35_g[:,j]
            col=wte_g@(vdir*lnf_w.to('cuda')); top=torch.topk(col,40).indices; bot=torch.topk(-col,40).indices
            a=(Hs64[rm].to('cuda')-mu_all[rm].to('cuda'))@vdir; sigma=float(a.std())
            flatidx=torch.topk(a.abs(),16).indices.tolist()
            seqs=[t//CERT_BLOCK for t in flatidx]; rows=torch.tensor(seqs,dtype=torch.long,device='cuda')
            ids_b=idg64[rows]; nP=len(flatidx)
            snap=[SnapHook(M["blocks"][L].attn,True) for L in range(nL)]
            ones=torch.ones(nP,CERT_BLOCK,device='cuda'); capb=[rm-1,rm]
            base,_=measure_class_snap_cap(M["m"],snap,ids_b,Pfull,vdir.contiguous(),ones,[top,bot],MB,capb)
            delt=torch.zeros(nP,2,2)
            for si,s in enumerate([1.0,-1.0]):
                fac=torch.ones(nP,CERT_BLOCK,device='cuda')
                for r,t in enumerate(flatidx):
                    a0=float(a[t]); pos=t%CERT_BLOCK
                    if abs(a0)>=A_EPS: fac[r,pos]=(a0+s*sigma)/a0
                mod_,_=measure_class_snap_cap(M["m"],snap,ids_b,Pfull,vdir.contiguous(),fac,[top,bot],MB,capb)
                for r,t in enumerate(flatidx):
                    pos=t%CERT_BLOCK; delt[r,si]=mod_[r,pos]-base[r,pos]
            for h in snap: h.close()
            dT=(delt[:,0,0]-delt[:,1,0])/2.0; dB=(delt[:,0,1]-delt[:,1,1])/2.0
            Cv=float((dT-dB).mean()); dev=abs(Cv-C_BANKED[j]["C"])
            ok=bool(dev<=TOL_ANCHOR)
            g4recs[f"j{j}"]={"C":round(Cv,5),"banked":C_BANKED[j]["C"],"dev":round(dev,5),"pass":ok}
            g4_ok=g4_ok and ok
            logln(f"[G4 j={j}] C={Cv:.5f} banked={C_BANKED[j]['C']} dev={dev:.5f} -> {'PASS' if ok else 'FAIL'}")
        del Hs64
        res["gates"]["G4_anchor_replay"]={"anchors":g4recs,"pass":bool(g4_ok)}; write_json()
        if not g4_ok:
            res["instrument_discrepancy"].append({"stage":"G4","name":"anchor_replay","why":g4recs})
            raise RuntimeError("G4 anchor replay FAILED -- clean kill")
    else: logln("[G4] SKIP (resume)")

    # ---------- G5: folded-cell byte-replay (code_b9) + identity-inject exact zero ----------
    if not res["gates"].get("G5_fold_replay",{}).get("pass"):
        gpu_free_check("G5")
        wteW_g=v1["wte_W"].float().to('cuda'); wtec_g=v1["wte_c"].float().to('cuda')
        ids_t=STREAMS["code"]; NHt=ids_t.shape[0]
        Yct=clean_logits(ids_t)
        Xc=CAPS["code"][9].to('cuda')-mu_all[9].to('cuda')
        Ecur_all=wte_g[ids_t.reshape(-1).to('cuda')]
        inj=InjectHook(M["blocks"][8])
        kl_id=inject_kl_full(ids_t,inj,torch.zeros(NHt,CERT_BLOCK,d,device='cuda'),Yct)
        b2P=(Xc@B2_g)@B2_g.t(); q35P=(Xc@Q35_g)@Q35_g.t()
        yhat=Ecur_all@wteW_g[9].t()+wtec_g[9]; y2=yhat-(yhat@B2_g)@B2_g.t(); y4=y2-(y2@Q35_g)@Q35_g.t()
        O_r=OB["O_r48_code_b9"].to('cuda')
        oP=(Xc@O_r)@O_r.t(); yk=y4-(y4@O_r)@O_r.t()
        kl48=inject_kl_full(ids_t,inj,(b2P+q35P+oP+yk-Xc).reshape(NHt,CERT_BLOCK,d),Yct)
        inj.close()
        dev=abs(kl48-CODE_B9_BANK)
        g5_ok=bool(kl_id==0.0 and dev<=TOL_REPLAY)
        res["gates"]["G5_fold_replay"]={"identity_kl":kl_id,"KL_r48":round(kl48,5),
                                        "banked":CODE_B9_BANK,"dev":round(dev,5),"pass":g5_ok}
        logln(f"[G5] id_kl={kl_id} r48={kl48:.5f} banked={CODE_B9_BANK} dev={dev:.5f} -> {'PASS' if g5_ok else 'FAIL'}")
        write_json()
        del Yct,Xc,b2P,q35P,yhat,y2,y4,oP,yk,Ecur_all; free()
        if not g5_ok:
            res["instrument_discrepancy"].append({"stage":"G5","name":"fold_replay","why":res["gates"]["G5_fold_replay"]})
            raise RuntimeError("G5 fold replay FAILED -- clean kill")
    else: logln("[G5] SKIP (resume)")

    # ---------- M1: mass table + candidates + dedup (frozen before battery) ----------
    if not res["mass"].get("done"):
        span5_c=span5
        mass={}
        for (reg,b,key,src) in FOLD_CELLS:
            H=(CAP_MASS_PROSE[b] if reg=="prose" else CAPS[reg][b])
            r=H-mu_all[b]
            r=r-(r@span5_c)@span5_c.t()
            O=OB[key]
            num=((r@O)**2).mean(0)                     # (n_dims,)
            den=float((r*r).sum(-1).mean())
            shares=(num/max(1e-12,den)).tolist()
            cand=[i for i,s in enumerate(shares) if s>=SHARE_MIN]
            if SMOKE: cand=cand[:SMOKE_FOLD_CAP]
            mass[key]={"cell":f"{reg}_b{b}","n_dims":O.shape[1],
                       "shares":[round(s,5) for s in shares],
                       "candidates":cand,"n_cand":len(cand),
                       "residue_share_below":round(sum(s for s in shares if s<SHARE_MIN),5)}
            logln(f"[M1 {key}] cell={reg}_b{b} cand={len(cand)} residue_below={mass[key]['residue_share_below']}")
        # dedup (locked order)
        words=[]
        for j in W_CORR_J:
            rm,dm=frozen[j]
            words.append({"wid":f"corr_j{j}","type":"corr","j":j,"room":rm,"dim":dm,"boundary":rm,
                          "jseed":j,"cell":None,"share":None,"aliases":[]})
        kept_fold=[]; n_alias_corr=0; n_alias_fold=0; fold_i=0
        for (reg,b,key,src) in FOLD_CELLS:
            order=sorted(mass[key]["candidates"],key=lambda i:-mass[key]["shares"][i])
            for i in order:
                o=OB[key][:,i]
                dots=(V35.t()@o).abs()
                if float(dots.max())>DEDUP_DOT:
                    jj=int(dots.argmax())
                    mass[key].setdefault("alias_of_corr",[]).append({"dim":i,"corr_j":jj,"dot":round(float(dots.max()),3)})
                    n_alias_corr+=1; continue
                hit=None
                for kf in kept_fold:
                    dd=abs(float(kf["vec"]@o))
                    if dd>DEDUP_DOT: hit=(kf,dd); break
                if hit is not None:
                    hit[0]["aliases"].append({"cell":mass[key]["cell"],"key":key,"dim":i,
                                              "share":mass[key]["shares"][i],"dot":round(hit[1],3)})
                    n_alias_fold+=1; continue
                kept_fold.append({"wid":f"fold_{key}_d{i}","type":"fold","key":key,"dim":i,
                                  "boundary":b,"cell":mass[key]["cell"],"jseed":100+fold_i,
                                  "share":mass[key]["shares"][i],"vec":o,"aliases":[]})
                fold_i+=1
        for kf in kept_fold: kf.pop("vec")
        words+=kept_fold
        res["mass"]={"done":True,"cells":mass,"n_alias_to_corridor":n_alias_corr,
                     "n_alias_cross_cell":n_alias_fold,"n_fold_words":len(kept_fold)}
        res["wordlist"]={"done":True,"n_words":len(words),"words":words}
        write_json()
        logln(f"[M1] words={len(words)} (corr {len(W_CORR_J)}, fold {len(kept_fold)}; "
              f"aliases corr={n_alias_corr} cross={n_alias_fold})")
    else: logln("[M1] SKIP (resume)")

    words=res["wordlist"]["words"]
    BASES["V35"]=V35; BASES["span5"]=span5
    for w in words:
        if w["type"]=="fold": BASES[f"vec_{w['wid']}"]=OB[w["key"]][:,w["dim"]].contiguous()
    save_bases()

    # ---------- M2: battery sweep ----------
    t_word=[]; bnull_now=B_NULL
    if res["budget"].get("bnull_downshift_at"):
        # resume-correctness: the pre-registered downshift fired earlier in THIS sweep; it stays
        # fired for all remaining W-FOLD words (uneven bars mid-category are not permitted)
        bnull_now=B_NULL_FAST
        logln(f"[budget] resume: downshift already fired at {res['budget']['bnull_downshift_at']} "
              f"-> B_NULL={B_NULL_FAST} held for remaining W-FOLD")
    for wi,w in enumerate(words):
        wid=w["wid"]
        if res["words"].get(wid,{}).get("done"): continue
        if el()>HARD_WALL_S:
            logln(f"[FB-WALL] hard wall at word {wid}; remaining UNRESOLVED"); break
        # predictive budget check (pre-registered contingency: STRICTER B_NULL=12 for remaining folds)
        rem=sum(1 for x in words[wi:] if not res["words"].get(x["wid"],{}).get("done"))
        if t_word and bnull_now==B_NULL:
            proj=el()+rem*(sum(t_word)/len(t_word))
            if proj>SOFT_COMPUTE_S:
                bnull_now=B_NULL_FAST
                res["budget"]["bnull_downshift_at"]=wid; res["budget"]["projected_s"]=round(proj,1)
                logln(f"[budget] projected {proj:.0f}s > soft wall -> B_NULL={B_NULL_FAST} (STRICTER bar) for remaining W-FOLD")
        tw0=time.time()
        vdir_g=(V35_g[:,w["j"]] if w["type"]=="corr" else BASES[f"vec_{wid}"].to('cuda'))
        bn=(bnull_now if w["type"]=="fold" else B_NULL)
        regs={}
        for regime in REGIMES:
            regs[regime]=word_battery(vdir_g,w["boundary"],regime,w["jseed"],bn,
                                      null_orth_q35=(w["type"]=="fold"),tag=wid)
        n_stable=sum(1 for r in regs.values() if r["stable"])
        stable_regs=[rg for rg in REGIMES if regs[rg]["stable"]]
        verdict="CERTIFIED-NO-GLOSS"
        if n_stable>=2: verdict="NAMED"
        elif (w["type"]=="fold" and n_stable==1 and w["cell"] is not None
              and stable_regs[0]==w["cell"].split("_b")[0]
              and regs[stable_regs[0]]["n_channels_clear"]>=2):
            verdict="NAMED-REGIME-SPECIFIC"
        rec={"done":True,"type":w["type"],"boundary":w["boundary"],"cell":w.get("cell"),
             "share":w.get("share"),"regimes":regs,"n_regimes_stable":n_stable,
             "stable_regimes":stable_regs,"verdict":verdict,"t_s":round(time.time()-tw0,1)}
        res["words"][wid]=rec; write_json(); save_bases()
        t_word.append(time.time()-tw0)
        logln(f"[M2 {wid} b{w['boundary']}] stable={stable_regs} verdict={verdict} "
              f"({rec['t_s']}s; {wi+1}/{len(words)})")
        free()

    # ---------- M3: verdict assembly ----------
    done_words={k:v for k,v in res["words"].items() if v.get("done")}
    unresolved=[w["wid"] for w in words if w["wid"] not in done_words]
    corr_named=sum(1 for k,v in done_words.items() if v["type"]=="corr" and v["verdict"].startswith("NAMED"))
    n_corr_done=sum(1 for v in done_words.values() if v["type"]=="corr")
    fold_done={k:v for k,v in done_words.items() if v["type"]=="fold"}
    fold_named=sum(1 for v in fold_done.values() if v["verdict"].startswith("NAMED"))
    frac_fold=(fold_named/len(fold_done)) if fold_done else None
    g=done_words.get("corr_j0",{})
    gv=g.get("verdict"); gn=g.get("n_regimes_stable")
    HLa=("BROAD-NAMES" if corr_named>=8 else ("SOME-NAMES" if corr_named>=3 else "NULL-HOLDS"))
    HLb=(None if frac_fold is None else
         ("VOCAB-RICH" if frac_fold>=0.5 else ("VOCAB-SPARSE" if frac_fold>=0.10 else "NOISE-FLOOR")))
    HLc=(None if not g else ("NAMED" if (gn or 0)>=2 else ("PARTIAL-NO-GLOSS" if gn==1 else "DEAF")))
    res["verdict"]={"done":True,"n_words":len(words),"n_done":len(done_words),
        "unresolved":unresolved,
        "H_L1_a":{"n_corr_named":corr_named,"n_corr_done":n_corr_done,"band":HLa,
                  "bands":"BROAD>=8 / SOME 3-7 / NULL<=2","bet":"SOME 45 / BROAD 30 / NULL 25"},
        "H_L1_b":{"n_fold_named":fold_named,"n_fold_done":len(fold_done),
                  "frac":(round(frac_fold,3) if frac_fold is not None else None),"band":HLb,
                  "bands":"RICH>=0.5 / SPARSE 0.10-0.50 / NOISE<0.10","bet":"SPARSE 50 / NOISE 30 / RICH 20"},
        "H_L1_c":{"glitch_verdict":gv,"n_regimes_stable":gn,"band":HLc,
                  "bands":"NAMED>=2 / PARTIAL=1 / DEAF=0","bet":"NAMED 55 / PARTIAL 30 / DEAF 15"}}
    res["status"]=("COMPLETE" if not unresolved else "COMPLETE-WITH-UNRESOLVED")
    if res["instrument_discrepancy"]: res["status"]="COMPLETE-WITH-DISCREPANCY" if not unresolved else "PARTIAL-WITH-DISCREPANCY"
    write_json(); save_bases()
    logln(f"[M3] H-L1-a={HLa} ({corr_named}/{n_corr_done}) H-L1-b={HLb} ({fold_named}/{len(fold_done)}) "
          f"H-L1-c={HLc} unresolved={len(unresolved)}")
    logln(f"L1 END status={res['status']} elapsed={el()}s"); logln("*** L1_DONE ***")
except Exception as e:
    import traceback
    res["status"]=f"ERROR: {e}"; res["trace"]=traceback.format_exc()[:3000]; write_json()
    logln(f"[L1] FATAL {e}"); logln(traceback.format_exc()); logln("*** L1_DONE ***")
finally:
    with open(os.path.join(DIR,"_l1_smoke_gpu.done" if SMOKE else "_l1_gpu.done"),"w") as f:
        f.write(res.get("status","?"))
