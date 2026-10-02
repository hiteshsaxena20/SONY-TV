# 🎮 SONY TV — Remote Access System

A secure, cross-platform remote-access system for Android TV.

## Components
- **TV Agent**: Kotlin / Android (`RemoteTV.apk`)
- **Relay Server**: FastAPI (`Cloud-hosted API`)
- **PC Client**: PySide6 (`RemoteTV-Setup.exe`)

## Project Structure
- `/server`: Relay Server (FastAPI)
- `/tv-app`: Android TV APK (Kotlin)
- `/pc-client`: Windows PC Client (PySide6)
- `/shared`: Shared protocol definitions
- `/docs`: Architecture and security documentation

Please refer to the `implementation_plan.md` for detailed phases and architecture.
