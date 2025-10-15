# Semantic Versioning Quick Reference

## 🚀 Quick Commands

```bash
# Check current version
python scripts/version_manager.py --current

# Bump patch (0.7.0 → 0.7.1)
python scripts/version_manager.py --bump patch

# Bump minor (0.7.0 → 0.8.0)
python scripts/version_manager.py --bump minor

# Bump major (0.7.0 → 1.0.0)
python scripts/version_manager.py --bump major

# Preview changes (dry run)
python scripts/version_manager.py --bump minor --dry-run
```

## 📝 Commit Message Cheat Sheet

| Type | Version | Example |
|------|---------|---------|
| `feat:` | Minor ↑ | `feat: add Redis caching` |
| `fix:` | Patch ↑ | `fix: resolve auth bug` |
| `perf:` | Patch ↑ | `perf: optimize queries` |
| `feat!:` | Major ↑ | `feat!: change API` |
| `docs:` | No change | `docs: update README` |
| `test:` | No change | `test: add unit tests` |
| `chore:` | No change | `chore: update deps` |

## 🎯 Version Bump Rules

| Change Type | Bump | Example |
|-------------|------|---------|
| Breaking changes | **Major** | 0.7.0 → **1.0.0** |
| New features | **Minor** | 0.7.0 → **0.8.0** |
| Bug fixes | **Patch** | 0.7.0 → **0.7.1** |
| Documentation | **None** | 0.7.0 → 0.7.0 |

## ⚡ Automated Flow

```
Commit with feat: → GitHub Actions → Bump minor → Update files → Create tag → Release
```

## 📖 Full Documentation

See [Semantic Versioning Guide](documentation/development/Semantic-Versioning.md) for complete details.
