# Pacman Database Synchronization Setup

The checkupdates.sh script expects the pacman/AUR databases to be synchronized,
but syncing requires root permissions. Rather than execute the script or waybar
as root, I choose to install a systemd servie which will periodically sync the
package repositories.

## Installation

### 1. Create the service file
Create `/etc/systemd/system/sync-package-dbs.service`:

```ini
[Unit]
Description=Synchronize pacman and AUR databases
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/pacman -Sy
User=root
```

### 2. Create the timer file
Create `/etc/systemd/system/sync-package-dbs.timer`:

```ini
[Unit]
Description=Synchronize pacman databases every 30 minutes
Requires=sync-package-dbs.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=30min
Persistent=true

[Install]
WantedBy=timers.target
```

### 3. Enable and start the timer
```bash
sudo systemctl daemon-reload
sudo systemctl enable sync-package-dbs.timer
sudo systemctl start sync-package-dbs.timer
```

## Configuration

### Timing Options
You can adjust the sync frequency by modifying the `OnUnitActiveSec` value in the timer file:

- `15min` - Every 15 minutes
- `30min` - Every 30 minutes (default)
- `1h` - Every hour
- `2h` - Every 2 hours

### Boot Delay
The `OnBootSec=5min` setting waits 5 minutes after boot before the first sync. You can adjust this value as needed.

## Management Commands

### Check timer status
```bash
sudo systemctl status sync-package-dbs.timer
```

### See when the timer will run next
```bash
systemctl list-timers sync-package-dbs.timer
```

### Stop the timer
```bash
sudo systemctl stop sync-package-dbs.timer
```

### Disable the timer
```bash
sudo systemctl disable sync-package-dbs.timer
```

### Manually trigger a sync
```bash
sudo systemctl start sync-package-dbs.service
```

## How It Works

1. The timer starts 5 minutes after boot
2. It runs `pacman -Sy` to sync package databases (without upgrading packages)
3. It repeats every 30 minutes
4. The `Persistent=true` setting ensures missed runs are executed when the system comes back online

## Notes

- This only syncs databases (`-Sy`), it does not upgrade packages (`-Syu`)
- The service requires root privileges to modify package databases
- Network connectivity is required for the sync to work
- Logs are available through journalctl for troubleshooting
