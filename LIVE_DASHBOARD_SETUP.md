# 🔴 D&D Live Dashboard - Setup Guide

Your D&D Virtual Tabletop now has **real-time live updates**! This guide will help you get everything running.

## 🎯 What You Get

### ✨ Live Features
- **🔴 Real-time DM Queue** - New player actions appear instantly without refresh
- **🗺️ Live Map Broadcasting** - When DM changes the map, all players see it immediately  
- **💬 Live Action Feed** - Approved actions broadcast to all players in real-time
- **📊 Live Queue Counter** - Badge updates automatically with pending submission count
- **🔔 Toast Notifications** - Beautiful alerts for important events
- **👁️ Connection Status** - Visual indicator showing live connection state

### 🎨 Enhanced UI/UX
- Smooth animations for new items
- Pulsing "LIVE" indicators
- Auto-updating queue badges
- Fade transitions for map changes
- Modern notification toasts

---

## 🚀 Quick Start (3 Options)

### Option 1: Full Real-time (Recommended - FREE)
Uses Supabase Realtime for instant updates via WebSockets

### Option 2: Polling Mode (Auto-fallback)
Updates every 3 seconds using HTTP polling (no setup needed)

### Option 3: Hybrid
Critical updates via Realtime, feed via polling

**The app works NOW in polling mode!** Add Supabase credentials to upgrade to real-time.

---

## 📋 Enabling True Real-time (Optional)

### Step 1: Get Supabase Credentials

You already have a Supabase project for database/storage. Now get the Realtime credentials:

1. **Go to Supabase Dashboard**: https://supabase.com/dashboard
2. **Select your project**
3. **Go to Settings → API**
4. Copy these two values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **Anon/Public Key** (starts with `eyJ...`)

### Step 2: Add to .env File

Open your `.env` file and add:

```env
# Supabase Realtime Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 3: Enable Realtime in Supabase

1. Go to **Database → Replication** in Supabase dashboard
2. Find `game_playerpost` table
3. Click the toggle to **enable replication**
4. That's it! ✅

### Step 4: Deploy/Restart

```bash
# Local development
python manage.py runserver

# Vercel (auto-deploys on git push)
git add .
git commit -m "Enable live dashboard"
git push
```

---

## 💰 Cost Breakdown

### Supabase Realtime Limits (Free Tier)
- ✅ **2 Million messages/month** (FREE)
- ✅ **500 concurrent connections** (FREE)
- ✅ **Unlimited channels** (FREE)

### Your Usage Estimate
**Typical 3-hour session (1 DM + 5 players):**
- 30 player submissions
- 25 approvals
- 5 map changes
- **= ~60 messages per session**

**Monthly (4 sessions):** 240 messages = **0.012%** of free allowance

**You'd need 33,000+ sessions/month to exceed free tier!** 🎉

---

## 🔧 How It Works

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Player Browsers                    │
│  (Dashboard, DM Review Panel, Multiple Players)     │
└──────────────┬──────────────────────┬───────────────┘
               │                      │
        HTTP (Forms/API)      WebSocket (Live Updates)
               │                      │
               ▼                      ▼
┌──────────────────────┐    ┌────────────────────┐
│   Vercel (Django)    │    │ Supabase Realtime  │
│  - Render templates  │    │ - DB change events │
│  - Process forms     │    │ - Broadcast updates│
│  - API endpoints     │    │ - Presence tracking│
└──────────┬───────────┘    └──────────┬─────────┘
           │                           │
           └────────► PostgreSQL ◄─────┘
                    (Supabase)
```

### Real-time Flow

1. **Player submits action** → Django saves to database
2. **Supabase detects change** → Broadcasts to all connected clients
3. **JavaScript receives event** → Updates UI instantly
4. **DM approves** → Status change broadcasts → Everyone sees update

### Fallback System

If Supabase credentials are missing or connection fails:
- ✅ Automatically switches to polling mode
- ✅ Updates every 3 seconds (configurable)
- ✅ No errors, seamless experience
- ⚠️ Slightly higher server load

---

## 🎮 Live Features Breakdown

### 1. Dashboard (`/`)
**DM View:**
- Real-time queue counter badge (red bubble shows count)
- Live action feed with slide-in animations
- Connection status indicator (green dot = live)
- Map changes broadcast to all players

**Player View:**
- See approved actions appear instantly
- Map updates in real-time
- Toast notifications for approvals
- Submission status feedback

### 2. DM Review Panel (`/review/`)
- New submissions appear with animation
- "LIVE" indicator with pulsing dot
- Toast notifications for new actions
- Auto-remove on approve/reject
- Empty state when queue is clear

### 3. API Endpoints (Auto-created)
- `/api/live-feed/` - Get approved actions
- `/api/pending-queue/` - Get DM queue (DM only)
- `/api/active-map/` - Get current map

---

## 🧪 Testing Live Updates

### Test 1: Live Queue (Need 2 browsers)
1. Open DM account in Browser A
2. Open Player account in Browser B
3. In Browser B: Submit an action
4. **Watch Browser A**: Badge updates + toast notification instantly!

### Test 2: Live Approvals
1. Browser A (DM): Approve the action
2. **Watch Browser B**: Action appears in feed instantly!
3. **Watch Browser B**: Toast: "✅ Your action was approved!"

### Test 3: Live Map Changes
1. Browser A (DM): Change map from dropdown
2. **Watch all player browsers**: Map fades and changes instantly!
3. **Watch all browsers**: Toast: "🗺️ Map changed to new scene!"

### Test 4: DM Review Panel
1. Open `/review/` in Browser A
2. Submit action from Browser B
3. **Watch Browser A**: New card slides in with glow!
4. Click approve
5. **Watch card**: Fades out smoothly

---

## 🐛 Troubleshooting

### "Using polling mode" in console
✅ **Expected!** This means Supabase credentials aren't set. Add them to `.env` to enable real-time.

### Updates not appearing
1. Check browser console for errors
2. Verify Supabase credentials in `.env`
3. Confirm database replication is enabled
4. Check network tab for WebSocket connection

### Connection indicator stays yellow/gray
1. **Yellow (connecting)**: Supabase is reachable but subscription pending
2. **Gray (disconnected)**: Falls back to polling (still works!)
3. **Green (connected)**: Real-time active! ✅

### JavaScript errors about Django template tags
✅ **Ignore these!** VS Code shows errors for `{% if %}` tags, but Django renders them correctly.

---

## 🎨 Customization

### Adjust Polling Interval
In `index.html` and `dm_review.html`, find:
```javascript
setInterval(() => {
    // ...
}, 3000); // Change 3000 to desired milliseconds
```

### Add Sound Effects
Uncomment in templates:
```javascript
function playNotificationSound() {
    const audio = new Audio('/static/sounds/notification.mp3');
    audio.volume = 0.3;
    audio.play().catch(e => console.log('Sound play failed:', e));
}
```
Add `.mp3` file to `game/static/sounds/notification.mp3`

### Change Toast Duration
In templates, find:
```javascript
setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
}, 4000); // Change 4000 to desired duration
```

### Disable Animations
Remove `animation: slideIn 0.3s ease-out;` from CSS

---

## 📊 Monitoring Usage

### Check Message Count (Development)
Open browser console on dashboard:
```javascript
// Watch real-time events
// They'll log automatically: "Database change detected: ..."
```

### Supabase Dashboard
1. Go to **Logs → Realtime** in Supabase
2. See connection count and message rate
3. Monitor for issues

---

## 🚀 Performance Tips

1. **Connection Pooling**: Reuse WebSocket connections (already implemented)
2. **Debouncing**: Rapid updates are batched (already implemented)
3. **Idle Disconnect**: Close connections when tab inactive (optional enhancement)
4. **Efficient Queries**: API endpoints limit to 50 items
5. **Image Optimization**: Use compressed images for maps

---

## 🔐 Security Notes

- ✅ Supabase Anon Key is **safe for client-side** use
- ✅ Row-Level Security (RLS) protects your data
- ✅ CSRF protection on all forms
- ✅ Login required for all endpoints
- ✅ DM-only actions verified server-side

---

## 📚 File Structure

```
game/
├── views.py                    # Django views + API endpoints
├── urls.py                     # URL routing (includes API)
├── models.py                   # Database models
├── context_processors.py       # Supabase config provider
├── templates/
│   ├── index.html             # Main dashboard (with live features)
│   ├── dm_review.html         # DM queue (with live features)
│   └── registration/
│       └── login.html
└── static/                    # CSS/JS (optional enhancements)

core/
└── settings.py                # Supabase configuration
```

---

## 🎯 Next Steps

### Immediate
1. ✅ Test in polling mode (already works!)
2. ✅ Add Supabase credentials to enable real-time
3. ✅ Test with multiple browsers
4. ✅ Deploy to Vercel

### Future Enhancements
- 🎲 **Dice Roller**: Shared dice with live results
- 💬 **Chat System**: Real-time DM-player messaging  
- ⚔️ **Initiative Tracker**: Live combat turn tracking
- 👥 **Presence Indicators**: See who's online with green dots
- 🔊 **Sound Effects**: Notification sounds for events
- 📱 **Mobile Optimization**: Better touch controls

---

## ❓ FAQ

**Q: Do I need Supabase Realtime?**
A: No! The app works great with polling mode. Realtime just makes it even better.

**Q: Will this cost money?**
A: No! Free tier covers typical D&D usage easily. See cost breakdown above.

**Q: What if Supabase goes down?**
A: App automatically falls back to polling. No downtime.

**Q: Can I use a different database?**
A: Yes, but you'd need to implement a different real-time solution (Django Channels, Pusher, etc.)

**Q: How many players can connect?**
A: Free tier supports 500 concurrent connections. More than enough!

---

## 🎉 You're All Set!

Your D&D dashboard is now **LIVE**! 

- ✅ Works immediately in polling mode
- ✅ Add Supabase credentials for true real-time
- ✅ Zero cost for typical usage
- ✅ Automatic fallback if issues occur
- ✅ Beautiful UI with animations

**Need help?** Check console logs for detailed debug info!

Happy gaming! 🎲⚔️🗺️
