# 🎲 Live Dashboard - Quick Reference

## ✅ What's Working NOW
Your dashboard has **live updates enabled**! Currently running in **polling mode** (updates every 3 seconds).

## 🚀 Run Locally
```bash
python manage.py runserver
```
Then open: http://127.0.0.1:8000/

## 🔴 Enable TRUE Real-time (Optional)

### 1. Get Supabase Keys
1. Go to https://supabase.com/dashboard
2. Settings → API
3. Copy **Project URL** and **Anon Key**

### 2. Add to .env
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJ...your_key_here...
```

### 3. Enable Database Replication
Supabase Dashboard → Database → Replication → Enable for `game_playerpost`

### 4. Restart Server
```bash
python manage.py runserver
```

Look for: **"🔴 Live updates active!"** toast notification

## 🎮 Live Features

### Dashboard (`/`)
- ✅ Live action feed (new approved actions appear automatically)
- ✅ Live map updates (DM changes map, everyone sees it)
- ✅ Queue badge counter (DMs see pending count)
- ✅ Toast notifications
- ✅ Connection status indicator

### DM Review Panel (`/review/`)
- ✅ Live queue updates (new submissions appear automatically)
- ✅ Animated card entrance
- ✅ Auto-remove on approve/reject
- ✅ Toast notifications

## 🧪 Test It

### Test 1: Live Queue
1. Open 2 browsers (one as DM, one as player)
2. Player submits action
3. **Watch DM browser**: Badge updates + notification!

### Test 2: Live Approval
1. DM approves action in review panel
2. **Watch player browser**: Action appears in feed!

### Test 3: Live Map
1. DM changes map from dropdown
2. **Watch all browsers**: Map changes instantly!

## 💰 Cost: $0
Free tier includes 2M messages/month. Your usage: ~0.01%

## 📖 Full Documentation
See `LIVE_DASHBOARD_SETUP.md` for complete guide.

## 🐛 Troubleshooting

**"Using polling mode"** → Normal! Add Supabase keys to enable real-time.

**Updates delayed?** → You're in polling mode (3-second refresh). Still works!

**No updates at all?** → Check browser console for errors.

---

**Happy Gaming! 🎲⚔️🗺️**
