# 🎭 Persona MCP - Advanced AI Persona Management System

**World's First MCP Persona Marketplace with Smart Context Detection, Persona Chaining, and 80%+ Token Savings**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/seanshin0214/persona-mcp?style=social)](https://github.com/seanshin0214/persona-mcp)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Community Personas](https://img.shields.io/badge/personas-26-blue)](https://github.com/seanshin0214/persona-mcp/tree/main/community)

An advanced persona management MCP server for Claude Desktop that revolutionizes how AI maintains specialized expertise while dramatically reducing token consumption.

<a href="https://glama.ai/mcp/servers/@seanshin0214/persona-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@seanshin0214/persona-mcp/badge" alt="Persona MCP server" />
</a>

---

## ✨ What is Persona MCP?

Persona MCP is a **Model Context Protocol (MCP) server** that allows you to:
- 🎯 **Switch between 26 world-class expert personas** on demand
- 🚢 **Save 80%+ tokens** with "Submarine Mode" (0 tokens until triggered)
- 🧠 **Smart context detection** - AI suggests the right persona automatically
- 🔗 **Chain personas** for multi-step workflows
- 🌍 **Community marketplace** - share and monetize your expertise

---

## 🚀 Key Features

### Core Capabilities
- **Submarine Mode**: Zero token consumption by default
- **Trigger-Based Activation**: Load personas only when needed via `@persona:name`
- **Individual File Management**: Each persona stored as a `.txt` file
- **Simple CRUD Operations**: Create, update, delete personas with MCP tools

### v2.0 Innovations
- **🧠 Smart Context Detection**: AI analyzes conversation and suggests optimal persona
- **🔗 Persona Chaining**: Execute multiple personas sequentially for complex tasks
- **📊 Usage Analytics**: Track patterns and improve recommendations (local storage only)
- **🌟 Community Collection**: 26 expert personas ready to use

---

## 💡 How Token Savings Work

### Traditional Approach (System Prompt)
```
Every conversation: 500 tokens consumed
100 conversations: 50,000 tokens wasted
Even when expertise isn't needed
```

### Persona MCP Approach
```
Default: 0 tokens (Submarine Mode)
When needed: @persona:name → Active only for that conversation
Next conversation: Back to 0 tokens
```

**Result**: 80%+ token savings in real-world usage

---

## 📦 Installation

### Prerequisites
- Claude Desktop
- Node.js 18+
- npm or yarn

### Steps

1. **Clone and Install**
```bash
git clone https://github.com/seanshin0214/persona-mcp.git
cd persona-mcp
npm install
```

2. **Configure Claude Desktop**

Edit `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac):

```json
{
  "mcpServers": {
    "persona": {
      "command": "node",
      "args": ["C:\\path\\to\\persona-mcp\\index.js"]
    }
  }
}
```

3. **Restart Claude Desktop**

---

## 🎯 Quick Start

### 1. Browse Community Personas

```
You: "Browse community personas"
Claude: [Executes browse_community tool]

🌟 Community Persona Collection

Found 26 personas

## Innovation & Technology
- innovation-expert
- ai-engineer
- fullstack-dev
...
```

### 2. Install a Persona

```
You: "Install innovation-expert persona"
Claude: [Executes install_community_persona]
✅ Persona "innovation-expert" installed successfully!
```

### 3. Use the Persona

```
You: "@persona:innovation-expert Analyze our product's disruption potential"
Claude: [Activates innovation expert persona and analyzes]
```

### 4. Smart Suggestions

```
You: "Explain quantum computing to a 10-year-old"
Claude: [Executes suggest_persona]
💡 Persona Suggestion
Recommended: @persona:science-teacher
Confidence: 85%
Reason: Educational context detected
```

---

## 🌟 Community Persona Collection

**26 world-class expert personas included!**

### Innovation & Technology (5)
- `innovation-expert` - Innovation strategy and disruption analysis
- `ai-engineer` - AI/ML engineering and architecture
- `fullstack-dev` - Full-stack web development
- `data-engineer` - Data pipelines and infrastructure
- `devops-engineer` - DevOps, CI/CD, cloud infrastructure

### Business & Strategy (6)
- `business-mgmt` - Business management and operations
- `strategy-consultant` - Strategic consulting and planning
- `product-manager` - Product management and roadmapping
- `vp-innovation` - VP of Innovation perspective
- `disruptive-entrepreneur` - Disruptive business models
- `global-startup` - Global startup strategy

### Education & Learning (7)
- `education-policy` - Education policy and reform
- `intl-education` - International education systems
- `student-mobility` - Student mobility and exchange programs
- `elite-tutor` - Elite tutoring and exam preparation
- `college-consultant` - College admissions consulting
- `university-president` - University leadership perspective
- `science-teacher` - Science education

### Analytics (2)
- `business-analytics` - Business data analysis
- `education-analytics` - Education data and metrics

### Professional Services (2)
- `harvard-law-dispute` - Harvard Law School dispute resolution
- `harvard-phd-negotiation` - Harvard PhD-level negotiation

### Example Personas (4)
- `python-master` - Python programming expert
- `creative-writer` - Creative writing and storytelling
- `product-strategist` - Product strategy
- `ux-design-expert` - UX design and user research

---

## 🛠️ Advanced Features

### Persona Chaining

Execute complex multi-step workflows:

```
You: "Chain these personas: coder → teacher → professional"

Step 1 - coder: Code analysis and bug detection
Step 2 - teacher: Explain findings to beginners
Step 3 - professional: Create formal report

✅ Chain completed: 3/3 steps
```

**Use Cases:**
- Code review → Documentation → Presentation
- Analysis → Summary → Executive brief
- Brainstorming → Structure → Final proposal

### Usage Analytics

```
You: "Show persona analytics"

📊 Persona Usage Analytics

Usage count:
  professional: 15 uses
  coder: 12 uses
  teacher: 8 uses

Top context patterns:
  professional: business, report, meeting
  coder: function, debug, implement
  teacher: explain, understand, learn

💡 Data stored locally only (never transmitted)
```

---

## 🔧 MCP Tools

### Basic Tools
1. **create_persona** - Create new persona
2. **update_persona** - Modify existing persona
3. **delete_persona** - Remove persona
4. **list_personas** - List all available personas

### Advanced Tools (v2.0)
5. **suggest_persona** - AI-powered persona recommendation
6. **chain_personas** - Sequential persona execution
7. **get_analytics** - View usage statistics
8. **browse_community** - Explore community collection
9. **install_community_persona** - One-click install from community

---

## 💡 Vision: Persona Marketplace

This is just the beginning! We're building the **world's first MCP Persona Marketplace**.

### Roadmap

**Phase 1 (Current):** GitHub Community
- ✅ 26 free personas
- ✅ Open source (MIT)
- ✅ Community contributions

**Phase 2 (In Development):** Persona Hub Website
- 🚧 Web-based marketplace
- 🚧 Search and discovery
- 🚧 One-click installation

**Phase 3 (Planned):** Creator Economy
- 💰 Premium personas
- 💰 70/30 revenue sharing (Creator/Platform)
- 💰 Monetize your expertise

See [VISION.md](VISION.md) for details.

---

## 🤝 Contributing

We welcome contributions! Share your expertise with the community.

### How to Contribute a Persona

1. Create persona following [community examples](community/)
2. Include metadata (Author, Category, Version)
3. Submit via [Persona Submission Issue](https://github.com/seanshin0214/persona-mcp/issues/new?template=persona_submission.md)
4. Or create a Pull Request

### Revenue Sharing Promise

**When Persona Hub launches:**
- 70% to Creator
- 30% to Platform
- Minimum payout: $50/month
- Monthly transparent reports

See [CONTRIBUTING.md](CONTRIBUTING.md) for full details.

---

## ❓ FAQ

### Does this cost money to use?

**No API costs.** Persona MCP is completely free to use. Unlike AI Council MCP (which calls multiple AI APIs), Persona MCP only manages text files on your local computer. It doesn't make any external API calls.

**What you need:**
- ✅ Claude Desktop (free or paid subscription)
- ✅ Node.js (free)
- ❌ No additional API keys required
- ❌ No pay-per-use costs

**Cost structure:**
- Persona MCP itself: **$0** (open source, MIT License)
- Running personas in Claude Desktop: Uses your existing Claude subscription
- The personas are just text prompts that enhance Claude's behavior

### Who pays for what?

**You:**
- Your Claude Desktop subscription (if using Claude Pro)
- No additional costs for Persona MCP

**Creator (@seanshin0214):**
- Does NOT pay for your Claude usage
- Does NOT collect any fees
- Provides this as free open-source software

### Is this a cloud service or SaaS?

**No.** Persona MCP runs entirely on your local computer.

**How it works:**
1. You download and install Persona MCP on your computer
2. Personas are stored as `.txt` files in `~/.persona/` folder
3. When you type `@persona:name`, it loads that text file
4. No data sent to external servers
5. Everything stays on your machine

### Do you collect any data?

**No.** Everything is local:
- ✅ Persona files stored locally (`~/.persona/`)
- ✅ Usage analytics stored locally (never transmitted)
- ✅ No telemetry, tracking, or data collection
- ✅ No central server to send data to
- ✅ Your privacy is 100% protected

### How is this different from ChatGPT custom GPTs?

**ChatGPT Custom GPTs:**
- Cloud-based, stored on OpenAI servers
- Requires ChatGPT Plus ($20/month)
- Limited to OpenAI ecosystem
- Can be shared publicly (privacy concerns)

**Persona MCP:**
- Runs locally on your computer
- Works with Claude Desktop (any tier)
- Open source and fully customizable
- 100% private (never leaves your machine)
- 80%+ token savings with Submarine Mode
- Community marketplace with revenue sharing

### Will the marketplace charge for personas?

**Current (Phase 1):**
- All 26 community personas are **FREE**
- MIT License (open source)

**Future (Phase 3 - Planned):**
- Premium personas may be offered by creators
- 70/30 revenue split (Creator gets 70%)
- Free personas will always remain available
- You choose what to download

**If you contribute a persona now:**
- It's free and open source (MIT)
- If marketplace launches, you're eligible for 70% revenue share on premium versions
- See [CONTRIBUTING.md](CONTRIBUTING.md) for details

---

## 📚 Documentation

- [VISION.md](VISION.md) - Long-term vision and roadmap
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines and revenue sharing
- [Community Personas](community/) - Browse all 26 personas

---

## 🐛 Troubleshooting

### MCP Server Not Showing

1. Completely quit and restart Claude Desktop
2. Check config file path: `%APPDATA%\Claude\claude_desktop_config.json`
3. Verify JSON syntax (commas, brackets)

### Persona Not Activating

- Use exact format: `@persona:name`
- Check persona name spelling
- Run `list_personas` to see available personas

### File Location Issues

**Windows:** `C:\Users\YourName\.persona\`
**Mac/Linux:** `~/.persona/`

Note: Folder may be hidden (enable "Show hidden files" in Explorer)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

Built with:
- [Model Context Protocol SDK](https://github.com/modelcontextprotocol/sdk) by Anthropic
- [docx](https://www.npmjs.com/package/docx) for Word export

Special thanks to all community contributors!

---

## 🔗 Links

- **GitHub**: https://github.com/seanshin0214/persona-mcp
- **Issues**: https://github.com/seanshin0214/persona-mcp/issues
- **Discussions**: https://github.com/seanshin0214/persona-mcp/discussions

---

**Created by**: @seanshin0214
**Version**: 2.0.0
**Last Updated**: 2025-11-02

🎭 **Join the Persona Revolution!** ⭐ Star the repo to support the project!