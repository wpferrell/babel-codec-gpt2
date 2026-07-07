# _l2babel.py -- L2 GRAMMAR ALL SEAMS (Babel Stage 2). PROPOSE-ONLY.
# Pre-registration: FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md ::
#   "L2 -- GRAMMAR ALL SEAMS (BABEL STAGE 2): PRE-REGISTRATION (2026-07-06)".
# Brief: BABEL_PROGRAM_BRIEF_2026-07-05.md STAGE 2 (fired by _relay_l2.bat on _l1.done).
# INSTRUMENT = _l3s1.py machinery VERBATIM (model loader fp32/eager/tf32-off/seed1234, forward-KL kernel
#   KL(clean||inj), YStore/clean_logits at MATCHED batch shape MB=4, identity sanity, EPS_KL=0.1871 floor,
#   ridge_fit/BLOCKWISE/MLP-CV/DOOR fits, InjectHook additive residual inject at BUS[b+1]) applied to all
#   12 seams b=0..11 x 3 regimes (prose/code/repetition) = 36 cells. Holistic certificate is verdict-bearing
#   per L3_FULL_PLAN redesign; per-field marginal reported. L3S1 prose (11,12)/(10,11) replay = the gate.
import json, time, os, math, traceback, gc, subprocess, hashlib
import torch, torch.nn.functional as Fnn

t0=time.time()
DIR=r"C:\Shadow\Dissector\D0_PROGRAM\CONSTRUCTIVE"
SMOKE=os.environ.get("L2B_SMOKE")=="1"
LOG=open(os.path.join(DIR,"_l2babel.log"),"a",encoding="utf-8")
def logln(s):
    s=str(s); LOG.write(f"[L2B {round(time.time()-t0,1):8.1f}s] "+s+"\n"); LOG.flush()
    try: print(s,flush=True)
    except Exception: pass
def el(): return round(time.time()-t0,1)
logln("="*100); logln(f"L2BABEL START smoke={SMOKE} torch={torch.__version__}")

# ---------------- locked constants (VERBATIM from _l3s1.py + _l1.py regime banks) ----------------
EPS_KL=0.1871
TIGHT=0.5*EPS_KL                        # 0.09355
CERT_BLOCK=512
N_FIT=64                                # fit (standing) blocks per regime
N_HOLD=16                               # certify (holdout) blocks per regime
MB=4                                    # inject/clean forwards batch = 4 seqs (matched shape)
CAP_CHUNK=16
RIDGE_REL=1e-3
MLP_WIDTHS=[8,32,128]; MLP_WD=[1e-5,1e-3,1e-1]; MLP_EPOCHS=400; MLP_PATIENCE=40
L2_BLOCKS=[[1,4,8,9,12,13],[0,10],[2,18],[3,7],[14,15],[5],[6],[11],[16],[17]]
BUDGET_HARD_S=8*3600
SOFT_WALL_S=4*3600                       # brief soft-wall; FB-1 budget contingency threshold
VOCAB_SANS_SPECIALS=50256; IND_SEG=64; REP_SEED=3
CODE_FIT_LO,CODE_FIT_HI=0,N_FIT*CERT_BLOCK               # humaneval fit  [0:32768)
CODE_HOLD_LO,CODE_HOLD_HI=N_FIT*CERT_BLOCK,(N_FIT+N_HOLD)*CERT_BLOCK  # humaneval hold [32768:40960)
PROSE_HOLD_LO,PROSE_HOLD_HI=8192,16384                   # wiki holdout (L3S1 verbatim)
REGIMES=["prose","code","repetition"]
NAMES=["naval/warship","collegiate-sports","special-symbol<->temporal-connective",
 "L0 magnitude/anomalous-token(numeric)","place-name<->statistics","clause-final/physical-process",
 "epistemic-negative","formula/markup-symbol","harm/casualty","sports-team","punctuation-boundary(struct)",
 "coastal-storm/geography","local-relation/admin","quotation/boundary","comma-boundary(struct)",
 "mixed-measurement","spatial-prep/@","hyphen/@-format","@-format"]
# pilot reproduction targets (L3S1 banked; gate tolerance)
GATE_TGT={"11":{"LINEAR":0.02536,"COPY":0.12538,"ABLATE":0.19071,"R2med":0.8627},
          "10":{"LINEAR":0.00684,"COPY":0.05513,"ABLATE":0.12975,"R2med":0.9219}}
GATE_TOL_KL=5e-3; GATE_TOL_R2=1e-2
REP_RUNG_SEAMS=[5,6,7]                   # executable rungs b5/b6/b7 (V6/V7) -> rep-regime seam entries

RESULT_JSON=os.path.join(DIR,"_l2babel_result_SMOKE.json" if SMOKE else "_l2babel_result.json")
MAPS_PT=os.path.join(DIR,"_l2babel_maps_SMOKE.pt" if SMOKE else "_l2babel_maps.pt")
GRAMMAR_JSON=os.path.join(DIR,"GRAMMAR_TABLE_V1_SMOKE.json" if SMOKE else "GRAMMAR_TABLE_V1.json")
torch.manual_seed(1234)

PEN=("FINDINGS_PEN_CONSTRUCTIVE_2026-06-28.md :: 'L2 -- GRAMMAR ALL SEAMS (BABEL STAGE 2):"
     " PRE-REGISTRATION (2026-07-06)'")
res={"experiment":"L2 GRAMMAR ALL SEAMS (Babel Stage 2): 12 seams x 3 regimes (GPT-2)",
     "date":"2026-07-06","propose_only":True,"pre_registration":PEN,
     "locked":{"eps_kl":EPS_KL,"tight":TIGHT,
        "verdict":"LINEAR-CERTIFIED iff KL_LIN<=0.1871 AND KL_LIN<KL_COPY; else rung=MLP; else BROKEN-AT-GRAIN",
        "seam_type":"PROPAGATION iff KL_COPY<=0.1871 else REWRITE",
        "bet":"MOSTLY-LINEAR(>=28) 45 / MIXED(12-27) 40 / MOSTLY-NONLINEAR(<12) 15",
        "gate":"prose (11,12)/(10,11) reproduce L3S1 pilot within KL 5e-3, R2 1e-2"},
     "config":{"n_fit":N_FIT,"n_hold":N_HOLD,"mb":MB,"cap_chunk":CAP_CHUNK,"ridge_rel":RIDGE_REL,
        "mlp_widths":MLP_WIDTHS,"mlp_wd":MLP_WD,"l2_blocks":L2_BLOCKS,"regimes":REGIMES,
        "precision":"fp32","tf32":"off","attn":"eager","seed":1234,"smoke":SMOKE},
     "gpu_free_checks":[],"instrument_discrepancy":[],"gate":{},"budget":{"per_field":True,"fb1_fired":False},
     "cells":{}, "status":"INIT"}

def write_json():
    res["elapsed_s"]=el(); tmp=RESULT_JSON+".tmp"
    with open(tmp,"w",encoding="utf-8") as f: json.dump(res,f,indent=1)
    os.replace(tmp,RESULT_JSON)
MAPS={}
def save_maps():
    tmp=MAPS_PT+".tmp"; torch.save(MAPS,tmp); os.replace(tmp,MAPS_PT)

# ---------------- resume ----------------
if os.path.exists(RESULT_JSON):
    try:
        prev=json.load(open(RESULT_JSON,encoding="utf-8"))
        for k in ("cells","gate","gpu_free_checks","instrument_discrepancy","budget"):
            if prev.get(k): res[k]=prev[k]
        logln(f"*** RESUME *** prior elapsed={prev.get('elapsed_s')} done cells={sorted(res['cells'].keys())}")
    except Exception as e: logln(f"resume load fail {e}")
if os.path.exists(MAPS_PT):
    try: MAPS=torch.load(MAPS_PT,map_location="cpu",weights_only=False); logln(f"*** RESUME maps {sorted(MAPS.keys())[:6]}...")
    except Exception as e: logln(f"maps load fail {e}"); MAPS={}
write_json()

# ---------------- GPU free-check (T16/L3S1 verbatim) ----------------
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

# ---------------- model (T16/L3S1 loader verbatim) ----------------
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

def load_objects():
    t15=torch.load(os.path.join(DIR,"_t15_bases.pt"),map_location="cpu",weights_only=False)
    C=t15["core_j0_5basis"].float()                       # [768,19] orthonormal
    t10=torch.load(os.path.join(DIR,"_t10_bases.pt"),map_location="cpu",weights_only=False)
    Qu=t10["Q_union"].float()                             # [768,385]
    orth=float((C.t()@C-torch.eye(C.shape[1])).norm())
    logln(f"[objects] C {tuple(C.shape)} ||C^TC-I||={orth:.2e} Qu{tuple(Qu.shape)}")
    res["config"]["core_orth_err"]=orth
    if orth>1e-4: res["instrument_discrepancy"].append({"stage":"objects","name":"core_orth","why":orth})
    return C,Qu

def build_regime_ids(regime,tok):
    """returns (fit_ids[N_FIT,512], hold_ids[N_HOLD,512]) verbatim from L1 regime banks."""
    if regime=="prose":
        wt=torch.load(os.path.join(DIR,"_t14_wt103_ids.pt"),map_location="cpu",weights_only=False)
        fit=ids_window(wt["ids"].tolist(),wt["lo"],wt["lo"]+N_FIT*CERT_BLOCK,"wt103 standing")
        WIKI=tok(load_wiki_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
        hold=ids_window(WIKI,PROSE_HOLD_LO,PROSE_HOLD_HI,"wiki holdout")
    elif regime=="code":
        CIDS=tok(load_code_text(),return_tensors=None,add_special_tokens=False)["input_ids"]
        fit=ids_window(CIDS,CODE_FIT_LO,CODE_FIT_HI,"humaneval fit")
        hold=ids_window(CIDS,CODE_HOLD_LO,CODE_HOLD_HI,"humaneval holdout")
    elif regime=="repetition":
        D=build_dind(N_FIT+N_HOLD,CERT_BLOCK,REP_SEED)
        fit=D[:N_FIT]; hold=D[N_FIT:N_FIT+N_HOLD]
    else: raise RuntimeError(regime)
    logln(f"[regime {regime}] fit{tuple(fit.shape)} hold{tuple(hold.shape)}")
    return fit,hold

# ---------------- capture residual reads at all boundaries (project onto C -> phi[b]) ----------------
def capture_phi_all(ids_cpu,C_g,tag):
    """phi[b] [ntok,19] cpu for b=0..12 (BUS0=drop out, BUS k=block k-1 out). VERBATIM L3S1."""
    model=M["m"]; nL=M["nL"]; N=ids_cpu.shape[0]; cch=min(N,CAP_CHUNK)
    buf={}; handles=[]
    def mk(key):
        def h(mod,inp,out): buf[key]=(out[0] if isinstance(out,tuple) else out).detach()
        return h
    handles.append(M["drop"].register_forward_hook(mk(0)))
    for L in range(nL): handles.append(M["blocks"][L].register_forward_hook(mk(L+1)))
    acc={b:[] for b in range(nL+1)}
    with torch.no_grad():
        for c0 in range(0,N,cch):
            c1=min(N,c0+cch); _=model(ids_cpu[c0:c1].to('cuda'),use_cache=False)
            for b in range(nL+1): acc[b].append((buf[b].reshape(-1,M["d"])@C_g).cpu())
    for hd in handles: hd.remove()
    phi={b:torch.cat(acc[b],0) for b in range(nL+1)}
    logln(f"[capture {tag}] phi boundaries={len(phi)} shape={tuple(phi[0].shape)}")
    return phi

def capture_bus_read(ids_cpu,b,Cmats,tag):
    """residual at BUS[b] projected onto each matrix in Cmats. returns list of [ntok,k]. VERBATIM L3S1."""
    model=M["m"]; N=ids_cpu.shape[0]; cch=min(N,CAP_CHUNK)
    store={}; handles=[]
    def h(mod,inp,out): store["r"]=(out[0] if isinstance(out,tuple) else out).detach()
    tgt = M["drop"] if b==0 else M["blocks"][b-1]
    handles.append(tgt.register_forward_hook(h))
    accs=[[] for _ in Cmats]
    with torch.no_grad():
        for c0 in range(0,N,cch):
            c1=min(N,c0+cch); _=model(ids_cpu[c0:c1].to('cuda'),use_cache=False)
            r=store["r"].reshape(-1,M["d"])
            for j,Cm in enumerate(Cmats): accs[j].append((r@Cm).cpu())
    for hd in handles: hd.remove()
    return [torch.cat(a,0) for a in accs]

# ---------------- forward-KL kernel (T16 verbatim: KL(clean||inj)) ----------------
def fkl(yt,yp):
    logp=Fnn.log_softmax(yt,-1); p=logp.exp(); lp=Fnn.log_softmax(yp,-1)
    return (p*(logp-lp)).sum(-1)

class InjectHook:
    def __init__(self,block):
        self.on=False; self.add=None
        self.handle=block.register_forward_hook(self._h)
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
            s1=min(N,s0+MB); lg=model(ids_cpu[s0:s1].to('cuda'),use_cache=False).logits.detach()
            outs.append(lg)
    return outs

def inject_kl(ids_cpu, injhook, C_g, delta_core, Yclean):
    model=M["m"]; N=ids_cpu.shape[0]; tot=0.0; cnt=0; ci=0
    with torch.no_grad():
        for s0 in range(0,N,MB):
            s1=min(N,s0+MB)
            dc=delta_core[s0:s1].to('cuda').float()
            injhook.add=(dc@C_g.t()); injhook.on=True
            lg=model(ids_cpu[s0:s1].to('cuda'),use_cache=False).logits
            injhook.on=False; injhook.add=None
            kl=fkl(Yclean[ci].float(),lg.float()); tot+=kl.sum().item(); cnt+=kl.numel(); ci+=1
            del lg,dc
    return tot/max(1,cnt)

# ---------------- fits (VERBATIM L3S1) ----------------
def ridge_fit(X,Y,rel):
    n=X.shape[0]; Xm=X.mean(0); Ym=Y.mean(0); Xc=X-Xm; Yc=Y-Ym
    G=Xc.t()@Xc/n; lam=rel*float(torch.linalg.eigvalsh(G).clamp(min=0).mean())
    p=X.shape[1]; A=Xc.t()@Xc+lam*n*torch.eye(p,dtype=X.dtype)
    W=torch.linalg.solve(A, Xc.t()@Yc).t()
    b=Ym - W@Xm
    return W,b,lam
def r2_cols(Yhat,Y):
    ss_res=((Y-Yhat)**2).sum(0); ss_tot=((Y-Y.mean(0))**2).sum(0).clamp(min=1e-12)
    return (1-ss_res/ss_tot)
class SmallMLP(torch.nn.Module):
    def __init__(self,w):
        super().__init__(); self.net=torch.nn.Sequential(torch.nn.Linear(19,w),torch.nn.GELU(),torch.nn.Linear(w,19))
    def forward(self,x): return self.net(x)
def mlp_train(Xtr,Ytr,Xva,Yva,w,wd,epochs,patience):
    dev=Xtr.device; net=SmallMLP(w).to(dev).float()
    opt=torch.optim.Adam(net.parameters(),lr=1e-2,weight_decay=wd)
    best=1e18; beststate=None; bad=0
    for ep in range(epochs):
        net.train(); opt.zero_grad(); loss=((net(Xtr)-Ytr)**2).mean(); loss.backward(); opt.step()
        net.eval()
        with torch.no_grad(): vl=((net(Xva)-Yva)**2).mean().item()
        if vl<best-1e-6: best=vl; beststate={k:v.detach().clone() for k,v in net.state_dict().items()}; bad=0
        else:
            bad+=1
            if bad>=patience: break
    if beststate: net.load_state_dict(beststate)
    return net,best

# ======================================================================================
#  CELL: fit 4 families at seam (b,b+1) in one regime + certify (holistic verdict-bearing)
# ======================================================================================
def run_cell(b, phi_fit, phi_hold, fit_ids, hold_ids, C_g, Qu_g, Yclean, per_field):
    label=f"b{b}"
    phiS_src=phi_fit[b].float(); phiS_tgt=phi_fit[b+1].float()
    phiH_src=phi_hold[b].float(); phiH_tgt=phi_hold[b+1].float()
    dS=capture_bus_read(fit_ids,b,[Qu_g],f"door-fit-{label}")[0]
    dH=capture_bus_read(hold_ids,b,[Qu_g],f"door-hold-{label}")[0]
    Nh=hold_ids.shape[0]; nseq_s=fit_ids.shape[0]
    def to3(x): return x.reshape(Nh,CERT_BLOCK,19)
    fits={}; preds={}
    # ---- F1 LINEAR ----
    W,bb,lam=ridge_fit(phiS_src,phiS_tgt,RIDGE_REL)
    yhat=phiH_src@W.t()+bb; preds["LINEAR"]=yhat
    sv=torch.linalg.svdvals(W)
    fits["LINEAR"]={"r2":[round(float(x),4) for x in r2_cols(yhat,phiH_tgt)],
        "lambda":lam,"singvals":[round(float(x),4) for x in sv],
        "rank_eff":float((sv/sv[0]).clamp(min=0).sum()) if sv[0]>0 else 0.0,
        "diag":[round(float(W[i,i]),4) for i in range(19)],
        "offdiag_rowE":[round(float((W[i]**2).sum()-W[i,i]**2)**0.5,4) for i in range(19)]}
    MAPS[f"W_{cur_regime}_b{b}"]=W.contiguous(); MAPS[f"bias_{cur_regime}_b{b}"]=bb.contiguous()
    # ---- F2 BLOCKWISE ----
    Wb=torch.zeros(19,19); bbk=torch.zeros(19)
    for blk in L2_BLOCKS:
        idx=torch.tensor(blk)
        Wk,bk,_=ridge_fit(phiS_src[:,idx],phiS_tgt[:,idx],RIDGE_REL)
        for a,i in enumerate(blk):
            for c,j in enumerate(blk): Wb[i,j]=Wk[a,c]
            bbk[i]=bk[a]
    yhatB=phiH_src@Wb.t()+bbk; preds["BLOCKWISE"]=yhatB
    fits["BLOCKWISE"]={"r2":[round(float(x),4) for x in r2_cols(yhatB,phiH_tgt)]}
    # ---- F3 MLP (ladder, seq-blocked 5-fold CV) ----
    Xs=phiS_src.to('cuda'); Ys=phiS_tgt.to('cuda'); Xh=phiH_src.to('cuda')
    per=Xs.shape[0]//nseq_s
    best=None
    if not SMOKE:
        segs=torch.arange(nseq_s).chunk(5)
        for w in MLP_WIDTHS:
            for wd in MLP_WD:
                cvs=[]
                for k in range(5):
                    va_seq=segs[k]; tr_seq=torch.cat([segs[j] for j in range(5) if j!=k])
                    def rows(seqs): return torch.cat([torch.arange(int(s)*per,int(s)*per+per) for s in seqs])
                    ri=rows(tr_seq).to('cuda'); vi=rows(va_seq).to('cuda')
                    net,vl=mlp_train(Xs[ri],Ys[ri],Xs[vi],Ys[vi],w,wd,MLP_EPOCHS,MLP_PATIENCE)
                    with torch.no_grad(): cvs.append(float(r2_cols(net(Xs[vi]),Ys[vi]).mean()))
                m=sum(cvs)/len(cvs)
                if best is None or m>best[0]: best=(m,w,wd)
    else:
        best=(0.0,8,1e-3)
    w_,wd_=best[1],best[2]
    segs=torch.arange(nseq_s).chunk(6); va_seq=segs[-1]; tr_seq=torch.cat([segs[j] for j in range(5)])
    def rows(seqs): return torch.cat([torch.arange(int(s)*per,int(s)*per+per) for s in seqs])
    ri=rows(tr_seq).to('cuda'); vi=rows(va_seq).to('cuda')
    net,_=mlp_train(Xs[ri],Ys[ri],Xs[vi],Ys[vi],w_,wd_,MLP_EPOCHS,MLP_PATIENCE)
    with torch.no_grad(): yhatM=net(Xh).cpu()
    preds["MLP"]=yhatM
    fits["MLP"]={"r2":[round(float(x),4) for x in r2_cols(yhatM,phiH_tgt)],
        "cv_best":{"width":w_,"wd":wd_,"cv_r2_mean":round(float(best[0]),4)}}
    # ---- F4 DOOR-MEDIATED (ridge from door reads at b; L2N positional null) ----
    Wd,bd,lamd=ridge_fit(dS,phiS_tgt,RIDGE_REL)
    yhatD=dH@Wd.t()+bd; preds["DOOR"]=yhatD
    g=torch.Generator().manual_seed(1234)
    permS=phiS_tgt.clone().reshape(nseq_s,per,19)
    for s in range(nseq_s):
        pr=torch.randperm(per,generator=g); permS[s]=permS[s][pr]
    permS=permS.reshape(-1,19)
    Wn,bn,_=ridge_fit(dS,permS,RIDGE_REL)
    yn=dS@Wn.t()+bn; nullr2=r2_cols(yn,permS)
    quel=[i for i in range(19) if float(nullr2[i])>=0.1]
    fits["DOOR"]={"r2":[round(float(x),4) for x in r2_cols(yhatD,phiH_tgt)],"door":"Q_union(385)",
        "positional_null_r2":[round(float(x),4) for x in nullr2],"quarantined_fields":quel}
    del Xs,Ys,Xh; free()
    logln(f"[{cur_regime} {label}] R2 LIN={sorted(fits['LINEAR']['r2'])[9]:.3f} BLK={sorted(fits['BLOCKWISE']['r2'])[9]:.3f} "
          f"MLP={sorted(fits['MLP']['r2'])[9]:.3f}(w{w_}) DOOR={sorted(fits['DOOR']['r2'])[9]:.3f} quel={len(quel)}")
    # ---- CERTIFY (inject at BUS[b+1]) ----
    injhook=InjectHook(M["blocks"][b])
    idkl=inject_kl(hold_ids,injhook,C_g,torch.zeros(Nh,CERT_BLOCK,19),Yclean)
    with torch.no_grad():
        injhook.add=torch.zeros(MB,CERT_BLOCK,M["d"],device='cuda'); injhook.on=True
        lg0=M["m"](hold_ids[:MB].to('cuda'),use_cache=False).logits; injhook.on=False
        iddl=float((lg0.float()-Yclean[0].float()).abs().max())
    sane=bool(idkl<=1e-9 and iddl<=1e-4)
    if not sane:
        res["instrument_discrepancy"].append({"stage":f"certify-{cur_regime}-{label}","name":"identity_inject",
            "why":f"KL={idkl} dl={iddl}"})
    phiH_src3=to3(phiH_src); phiH_tgt3=to3(phiH_tgt)
    abl_mean=phiH_tgt.mean(0)
    fam_list=["LINEAR","BLOCKWISE","MLP","DOOR"]
    def delta_single(pred3,i):
        d=torch.zeros(Nh,CERT_BLOCK,19); d[:,:,i]=pred3[:,:,i]-phiH_tgt3[:,:,i]; return d
    D={f:{} for f in fam_list}; Dcopy={}; Dabl={}
    if per_field:
        for i in range(19):
            pc=to3(phiH_src); Dcopy[i]=inject_kl(hold_ids,injhook,C_g,delta_single(pc,i),Yclean)
            pa=phiH_tgt3.clone(); pa[:,:,i]=abl_mean[i]
            Dabl[i]=inject_kl(hold_ids,injhook,C_g,delta_single(pa,i),Yclean)
            for f in fam_list:
                p3=to3(preds[f]); D[f][i]=inject_kl(hold_ids,injhook,C_g,delta_single(p3,i),Yclean)
            write_json()
    # holistic all-19 per family (VERDICT-BEARING) + copy + ablate nulls
    holistic={}
    for f in fam_list:
        p3=to3(preds[f]); dfull=p3-phiH_tgt3
        holistic[f]=inject_kl(hold_ids,injhook,C_g,dfull,Yclean)
    dcopyf=phiH_src3-phiH_tgt3; holistic["COPY"]=inject_kl(hold_ids,injhook,C_g,dcopyf,Yclean)
    dablf=phiH_tgt3.clone()*0
    for i in range(19): dablf[:,:,i]=abl_mean[i]-phiH_tgt3[:,:,i]
    holistic["ABLATE"]=inject_kl(hold_ids,injhook,C_g,dablf,Yclean)
    injhook.close(); free()
    # ---- VERDICT (holistic; locked bands) ----
    kl_lin=holistic["LINEAR"]; kl_copy=holistic["COPY"]; kl_mlp=holistic["MLP"]
    seam_type="PROPAGATION" if kl_copy<=EPS_KL else "REWRITE"
    if kl_lin<=EPS_KL and kl_lin<kl_copy:
        verdict="LINEAR-CERTIFIED"; band=("TIGHT" if kl_lin<=TIGHT else "CERTIFIED"); rung=None
    else:
        if kl_mlp<=EPS_KL and kl_mlp<kl_copy:
            verdict="NONLINEAR-CERTIFIED-VIA-RUNG"; band="RUNG-MLP"; rung="MLP"
        else:
            verdict="BROKEN-AT-GRAIN"; band=None; rung="MLP-tried"
    exec_rung = (cur_regime=="repetition" and b in REP_RUNG_SEAMS)
    r2=fits["LINEAR"]["r2"]; r2s=sorted(r2)
    logln(f"[{cur_regime} {label}] VERDICT {verdict} ({band}) seam={seam_type} | "
          f"LIN={kl_lin:.4f} COPY={kl_copy:.4f} MLP={kl_mlp:.4f} ABL={holistic['ABLATE']:.4f} id={'OK' if sane else 'FAIL'}")
    return {"regime":cur_regime,"hop":[b,b+1],"verdict":verdict,"fidelity_band":band,"seam_type":seam_type,
            "rung":rung,"executable_rung_provenance":exec_rung,
            "holistic":{k:round(v,5) for k,v in holistic.items()},
            "linear_r2":{"median":round(r2s[9],4),"min":round(min(r2),4),"max":round(max(r2),4)},
            "linear_rank_eff":round(fits["LINEAR"]["rank_eff"],3),
            "linear_singvals":fits["LINEAR"]["singvals"],
            "linear_diag":fits["LINEAR"]["diag"],"linear_offdiag_rowE":fits["LINEAR"]["offdiag_rowE"],
            "mlp_cv":fits["MLP"]["cv_best"],"door_quarantined":len(quel),
            "identity_kl":idkl,"identity_dlogit":iddl,"identity_pass":sane,
            "per_field":{"D":{f:{str(i):round(D[f][i],5) for i in D[f]} for f in D},
                         "copy":{str(i):round(Dcopy[i],5) for i in Dcopy},
                         "ablate":{str(i):round(Dabl[i],5) for i in Dabl}} if per_field else "SKIPPED-FB1",
            "fits_r2":{f:fits[f]["r2"] for f in fam_list}}

# ======================================================================================
# MAIN
# ======================================================================================
cur_regime=None
try:
    ensure_model()
    C,Qu=load_objects()
    C_g=C.to('cuda').float(); Qu_g=Qu.to('cuda').float()
    MAPS["C"]=C.contiguous(); save_maps(); write_json()
    nL=M["nL"]  # 12
    HOPS=list(range(nL))  # 0..11
    # cell order: prose gate hops first (11,10) -> fail fast, then prose 0..9, then code, then repetition
    prose_order=[11,10]+[b for b in range(nL) if b not in (10,11)]
    plan=[("prose",b) for b in prose_order]
    if not SMOKE:
        plan+=[("code",b) for b in HOPS]+[("repetition",b) for b in HOPS]
    else:
        plan=[("prose",11),("prose",10)]

    gpu_free_check("start")
    for reg in (["prose"] if SMOKE else REGIMES):
        # capture phi once per regime (fit+hold); door captured per cell (verbatim L3S1)
        need=[c for c in plan if c[0]==reg and f"{reg}:{c[1]}" not in res["cells"]]
        if not need:
            logln(f"[{reg}] all cells done -> skip capture"); continue
        cur_regime=reg
        fit_ids,hold_ids=build_regime_ids(reg,M["tok"])
        gpu_free_check(f"capture-{reg}")
        phi_fit=capture_phi_all(fit_ids,C_g,f"fit-{reg}")
        phi_hold=capture_phi_all(hold_ids,C_g,f"hold-{reg}")
        Yclean=clean_logits(hold_ids)
        for (rg,b) in [c for c in plan if c[0]==reg]:
            key=f"{reg}:{b}"
            if key in res["cells"]:
                logln(f"[skip] {key} already done"); continue
            # FB-1 budget: drop report-only per-field if projected wall exceeds soft-wall
            per_field=res["budget"]["per_field"]
            if SMOKE: per_field=False   # smoke validates holistic/gate path fast
            if per_field and not SMOKE:
                done_n=len(res["cells"]);
                if done_n>=1:
                    avg=el()/max(1,done_n); remaining=(36-done_n)
                    if el()+avg*remaining>SOFT_WALL_S and el()>600:
                        res["budget"]["per_field"]=False; res["budget"]["fb1_fired"]=True; per_field=False
                        logln(f"[FB-1] projected {el()+avg*remaining:.0f}s > soft wall {SOFT_WALL_S}s -> drop per-field marginal (report-only)")
            tc=time.time()
            cell=run_cell(b,phi_fit,phi_hold,fit_ids,hold_ids,C_g,Qu_g,Yclean,per_field)
            cell["t_s"]=round(time.time()-tc,1); cell["per_field_kept"]=per_field
            res["cells"][key]=cell
            save_maps(); write_json()
            # GATE: after prose 11 & 10 both done, verify reproduction vs pilot
            if reg=="prose" and b in (11,10) and not res["gate"].get("checked") \
               and "prose:11" in res["cells"] and "prose:10" in res["cells"]:
                gate={"checked":True,"pass":True,"detail":{}}
                for bb2 in ("11","10"):
                    h=res["cells"][f"prose:{bb2}"]["holistic"]; tgt=GATE_TGT[bb2]
                    r2m=res["cells"][f"prose:{bb2}"]["linear_r2"]["median"]
                    d={"dLIN":round(abs(h["LINEAR"]-tgt["LINEAR"]),5),"dCOPY":round(abs(h["COPY"]-tgt["COPY"]),5),
                       "dABL":round(abs(h["ABLATE"]-tgt["ABLATE"]),5),"dR2":round(abs(r2m-tgt["R2med"]),4),
                       "id_kl":res["cells"][f"prose:{bb2}"]["identity_kl"]}
                    ok=(d["dLIN"]<=GATE_TOL_KL and d["dCOPY"]<=GATE_TOL_KL and d["dABL"]<=GATE_TOL_KL
                        and d["dR2"]<=GATE_TOL_R2 and res["cells"][f"prose:{bb2}"]["identity_pass"])
                    d["pass"]=bool(ok); gate["detail"][bb2]=d; gate["pass"]=gate["pass"] and ok
                res["gate"]=gate; write_json()
                logln(f"[GATE] {json.dumps(gate)}")
                if not gate["pass"] and not SMOKE:
                    res["status"]="GATE-FAIL"; write_json()
                    raise RuntimeError(f"GATE FAILED (L3S1 reproduction) -- clean kill: {gate['detail']}")
        del phi_fit,phi_hold,Yclean,fit_ids,hold_ids; free()

    # ---------- assemble GRAMMAR_TABLE_V1 + verdict rollup ----------
    if not SMOKE and len([k for k in res["cells"]])>=36:
        cells=res["cells"]
        lin=sum(1 for k in cells if cells[k]["verdict"]=="LINEAR-CERTIFIED")
        rung=sum(1 for k in cells if cells[k]["verdict"]=="NONLINEAR-CERTIFIED-VIA-RUNG")
        broke=sum(1 for k in cells if cells[k]["verdict"]=="BROKEN-AT-GRAIN")
        rewrite=sum(1 for k in cells if cells[k]["seam_type"]=="REWRITE")
        prop=sum(1 for k in cells if cells[k]["seam_type"]=="PROPAGATION")
        tight=sum(1 for k in cells if cells[k]["fidelity_band"]=="TIGHT")
        bet=("MOSTLY-LINEAR" if lin>=28 else ("MIXED" if lin>=12 else "MOSTLY-NONLINEAR"))
        bet_hit=(bet=="MOSTLY-LINEAR")  # favorite was MOSTLY-LINEAR 45
        # per-seam regime stability of the LINEAR verdict
        stab={}
        for b in HOPS:
            vs=[cells[f"{r}:{b}"]["verdict"] for r in REGIMES]
            stab[str(b)]={"verdicts":vs,"all_linear":all(v=="LINEAR-CERTIFIED" for v in vs),
                          "agree":len(set(vs))==1}
        regime_stable=sum(1 for b in HOPS if stab[str(b)]["agree"])
        table={"frozen":True,"instrument":"L3S1 verbatim","eps_kl":EPS_KL,
               "n_cells":len(cells),"n_linear":lin,"n_rung":rung,"n_broken":broke,
               "n_tight":tight,"n_propagation":prop,"n_rewrite":rewrite,
               "bet":res["locked"]["bet"],"bet_outcome":bet,"bet_favorite_hit":bet_hit,
               "regime_stable_seams":regime_stable,"per_seam_regime_stability":stab,
               "cells":{k:{"regime":cells[k]["regime"],"hop":cells[k]["hop"],"verdict":cells[k]["verdict"],
                           "fidelity_band":cells[k]["fidelity_band"],"seam_type":cells[k]["seam_type"],
                           "holistic":cells[k]["holistic"],"linear_r2":cells[k]["linear_r2"],
                           "linear_rank_eff":cells[k]["linear_rank_eff"],
                           "executable_rung_provenance":cells[k]["executable_rung_provenance"]}
                         for k in sorted(cells.keys())}}
        tmp=GRAMMAR_JSON+".tmp"
        with open(tmp,"w",encoding="utf-8") as f: json.dump(table,f,indent=1)
        os.replace(tmp,GRAMMAR_JSON)
        gh=hashlib.sha256(open(GRAMMAR_JSON,"rb").read()).hexdigest()[:16]
        res["grammar_table_v1"]={"file":os.path.basename(GRAMMAR_JSON),"sha256_16":gh,
            "n_linear":lin,"n_rung":rung,"n_broken":broke,"n_propagation":prop,"n_rewrite":rewrite,
            "bet_outcome":bet,"bet_favorite_hit":bet_hit,"regime_stable_seams":regime_stable}
        MAPS["grammar_table_sha"]=gh; save_maps()
        logln(f"[GRAMMAR_TABLE_V1] sha={gh} LINEAR={lin} RUNG={rung} BROKEN={broke} "
              f"PROP={prop} REWRITE={rewrite} bet={bet} regime_stable={regime_stable}/12")

    if SMOKE:
        c11=res["cells"].get("prose:11"); ok=bool(c11 and c11["identity_pass"] and res["gate"].get("pass"))
        res["status"]="SMOKE-"+("OK" if ok else "FAIL")
        res["S0_smoke"]={"gate":res["gate"],"prose11_verdict":(c11 or {}).get("verdict")}
        logln(f"[SMOKE] gate={res['gate'].get('pass')} -> {res['status']}")
    else:
        done=len(res["cells"])>=36 and res.get("grammar_table_v1") and res["gate"].get("pass")
        res["status"]=("COMPLETE" if (done and not res["instrument_discrepancy"]) else
                       ("COMPLETE-WITH-DISCREPANCY" if done else "PARTIAL"))
    save_maps(); write_json()
    if M["m"] is not None: del M["m"]; M["m"]=None; free()
except Exception as e:
    res["fatal_error"]={"error":str(e),"trace":traceback.format_exc()}
    logln(f"FATAL {e}\n{traceback.format_exc()}"); res.setdefault("status","FATAL")
write_json()
logln(f"L2BABEL END status={res.get('status')} elapsed={el()}s cells={len(res['cells'])}")
open(os.path.join(DIR,"_l2babel_smoke_gpu.done" if SMOKE else "_l2babel_gpu.done"),"w").write(str(res.get("status","?"))+"\n")
logln("*** L2BABEL_"+("SMOKE_" if SMOKE else "")+"DONE ***"); LOG.flush(); LOG.close(); print("done")
