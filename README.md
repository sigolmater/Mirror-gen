# Mirror-gen

cd /path/to/your/repo
git branch -M main
git pull origin main || true
mkdir -p results scripts
mv results.csv placement_report.json load_sim.csv results/  # 파일 위치 정리
git add results scripts
git commit -m "share: results update"
git push origin main