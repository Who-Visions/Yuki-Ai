# Yuki System - Quick Reference

## 🚀 How to Use

### Generate Images (DB-First Method)
```bash
python db_first_generator.py
```

### View Logged Errors & Learnings
```bash
python error_learning_log.py
```

### Check Test Results
- Jesse: `c:\Yuki_Local\jesse_test_results\` (10 images)
- Nadley: `c:\Yuki_Local\nadley_db_results\` (7 images)

## 📊 Key Stats
- **Speed**: ~56 seconds per image
- **Cost**: ~$0.13 per image  
- **API Efficiency**: 72.5% reduction in calls
- **Success Rate**: 15/15 images verified saved

## 🛡️ Critical Rules (ALWAYS APPLY)
1. ✅ Run perspective correction first
2. ✅ Preserve race, ethnicity, gender explicitly
3. ✅ Filter characters by gender
4. ✅ Verify files saved (file.exists() check)
5. ✅ Use local DB before API calls

## 📁 Important Files
- `facial_geometry_corrector.py` - Fix perspective distortion
- `db_first_generator.py` - Main generation system
- `error_learning_log.py` - All errors & fixes
- `SESSION_LOG_2025-12-02.md` - Full session details

## 🐛 Known Issues (FIXED)
- ✅ Identity loss (race change) - FIXED with explicit preservation
- ✅ Nose enlargement - FIXED with perspective correction
- ✅ Ghost API calls - FIXED with verification
- ⚠️ Quota limits - MITIGATED with DB-first approach

## 📞 Quick Help
For full documentation, see: `SESSION_LOG_2025-12-02.md`
