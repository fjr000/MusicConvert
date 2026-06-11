# 加密音频处理方案调研

## 当前方案

### MusicDecrypto
- **项目**: [davidxuang/MusicDecrypto](https://github.com/davidxuang/MusicDecrypto)
- **版本**: v2.4.2
- **语言**: C# (.NET)
- **许可证**: LGPL-2.1 (核心库), AGPL-3.0 (CLI/GUI)
- **部署方式**: Windows x64 可执行文件 (musicdecrypto.exe)

#### 优点
- 成熟稳定，活跃维护
- 支持格式全面 (NCM, QMC, KGM, TM, MGG, VPR, KWM, X2M/X3M 等)
- 独立进程运行，不影响主程序稳定性
- CLI 接口简单，易于集成
- 支持自动格式检测 (-x 参数)

#### 缺点
- Windows 平台专属（.NET 依赖）
- 需要额外分发 EXE 文件
- 进程间调用有性能开销
- 许可证为 AGPL-3.0（CLI），传染性较强

## 备选方案

### 1. unlock-music (Web/JS)
- **项目**: [unlock-music/unlock-music](https://github.com/unlock-music/unlock-music)
- **语言**: TypeScript/JavaScript
- **部署**: 纯前端实现

**评估**:
- ❌ 主要为浏览器设计，不适合后端批处理
- ❌ Node.js 集成需要额外构建
- ✓ 许可证相对宽松 (MIT)

### 2. Python 直接实现
搜索 PyPI 包：ncm-decrypt, qmc-decrypt 等

**评估**:
- ✓ 无需外部依赖，打包更简单
- ✓ 性能更好（无进程调用开销）
- ❌ 现有 Python 库不成熟，格式支持有限
- ❌ 需要自己维护解密逻辑
- ⚠️ 法律风险：直接集成解密代码可能更敏感

### 3. Rust CLI 工具
如 parakeet-crypto-rs 等

**评估**:
- ✓ 性能优秀
- ✓ 跨平台支持
- ❌ 生态不如 C# 成熟
- ❌ 项目活跃度较低

## 结论

**继续使用 MusicDecrypto 是当前最优选择**，理由如下：

1. **格式支持最全面**: 覆盖所有主流加密格式
2. **稳定性有保障**: 项目活跃维护，问题修复及时
3. **集成成本低**: 现有方案已验证可行
4. **隔离风险**: 独立进程运行，主程序不受影响
5. **许可证可接受**: AGPL-3.0 虽然传染性强，但仅限于解密工具本身，主程序调用不受影响（进程边界隔离）

### 未来改进方向

如果需要跨平台支持，可以考虑：
- 调研 unlock-music 是否有成熟的 Node.js 后端实现
- 等待 Rust 生态成熟后迁移
- 自行实现核心格式（仅 NCM/QMC）的 Python 解密，保持 MusicDecrypto 作为补充

但**短期内无需改动**，当前方案已经满足 Windows 便携版的设计目标。
