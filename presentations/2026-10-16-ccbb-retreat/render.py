"""Render each slide of a pptx to PNG via QuickLook (first-slide thumbnail of single-slide copies)."""
import os, re, shutil, subprocess, sys, zipfile
src, outdir = sys.argv[1], sys.argv[2]
only = set(int(a) for a in sys.argv[3:])
shutil.rmtree(outdir, ignore_errors=True); os.makedirs(outdir)
z = zipfile.ZipFile(src)
pres = z.read("ppt/presentation.xml").decode()
ids = re.findall(r"<p:sldId [^>]*/>", pres)
for n, sid in enumerate(ids, 1):
    if only and n not in only: continue
    p2 = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>", f"<p:sldIdLst>{sid}</p:sldIdLst>", pres, flags=re.S)
    tmp = os.path.join(outdir, f"s{n:02d}.pptx")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as o:
        for item in z.infolist():
            data = p2.encode() if item.filename == "ppt/presentation.xml" else z.read(item.filename)
            o.writestr(item.filename, data)
    subprocess.run(["qlmanage", "-t", "-s", "1600", "-o", outdir, tmp], capture_output=True)
    os.rename(tmp + ".png", os.path.join(outdir, f"s{n:02d}.png")); os.remove(tmp)
print("\n".join(sorted(os.path.join(outdir, f) for f in os.listdir(outdir))))
