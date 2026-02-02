# 🐛 Known Issues and Solutions

## Critical Issues

### Issue #1: Orphaned Worker Processes

**Problem:**
When using `quick_start_all_files.py`, if you close the terminal or the script crashes, multiprocessing worker processes continue running in the background, consuming RAM (up to 3.5 GB).

**Why it happens:**
- Python's `multiprocessing.Pool` creates worker processes
- When parent process dies unexpectedly, workers don't auto-terminate
- Workers keep consuming RAM until manually killed

**Solution (Implemented in v1.1):**
Added proper cleanup handlers:
- `atexit` handler to terminate pool on exit
- `finally` block to ensure cleanup
- Timeout on `pool.join()` to prevent hanging

**Manual cleanup if needed:**
```powershell
# Windows
Stop-Process -Name python -Force

# Linux/Mac
pkill -9 python
```

**Prevention:**
- Always let scripts finish naturally
- Use Ctrl+C (which now properly cleans up)
- Monitor Task Manager/Activity Monitor

---

## Minor Issues

### Issue #2: Slow Feature Extraction

**Problem:** Processing 10,000+ files takes 2-4 hours

**Why:** `music21` library is comprehensive but slow

**Solutions:**
- ✅ Parallel processing (already implemented)
- ✅ Auto-save every 100 files (prevents data loss)
- Consider: Caching, faster MIDI parser

---

### Issue #3: Low Model Accuracy (20%)

**Problem:** Demo model has low accuracy

**Why:** Using random labels for demonstration

**Solution:** 
1. Manually label your MIDI files
2. Create `labels.csv` with real categories
3. Retrain model
4. Expected accuracy: 60-80% with real labels

---

## Monitoring

### Check for Orphaned Processes

**Windows:**
```powershell
Get-Process python | Select-Object Id, CPU, WorkingSet
```

**Linux/Mac:**
```bash
ps aux | grep python
```

### Monitor RAM Usage

**Windows:**
```powershell
Get-WmiObject Win32_OperatingSystem | Select-Object FreePhysicalMemory
```

**Linux/Mac:**
```bash
free -h
```

---

## Best Practices

1. **Always use virtual environment** - Isolates dependencies
2. **Monitor RAM** - Especially with large datasets
3. **Use auto-save** - Prevents data loss
4. **Close properly** - Don't force-kill terminals
5. **Check processes** - After running scripts

---

## Reporting Issues

If you encounter issues:

1. Check this document first
2. Search existing GitHub issues
3. Create new issue with:
   - Python version
   - OS and version
   - Error message
   - Steps to reproduce

---

**Last updated:** 2026-02-02
