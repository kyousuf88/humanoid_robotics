# Troubleshooting Section Template (FR-022)

Use this template for the troubleshooting section at the end of each module.

```markdown
---
sidebar_position: 99
---

# Troubleshooting: Module [N] - [Title]

This guide covers common issues encountered when working with [module topic].

## Quick Diagnosis

| Symptom | Likely Cause | Jump To |
|---------|--------------|---------|
| [Symptom 1] | [Brief cause] | [#issue-name](#issue-name) |
| [Symptom 2] | [Brief cause] | [#issue-name](#issue-name) |
| [Symptom 3] | [Brief cause] | [#issue-name](#issue-name) |

## Common Issues

### Issue: [Problem Description] {#issue-name}

**Symptoms**:
- [What the user observes]
- [Error messages if applicable]

**Cause**:
[Explanation of why this happens]

**Solution**:

1. [Step 1]
2. [Step 2]
3. [Step 3]

```bash
# Example fix command
[command to fix the issue]
```

**Prevention**:
[How to avoid this issue in the future]

---

### Issue: [Problem Description] {#issue-name-2}

**Symptoms**:
- [What the user observes]

**Cause**:
[Explanation]

**Solution**:

1. [Step 1]
2. [Step 2]

---

## Error Messages Reference

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `[Error text]` | [Why it occurs] | [Brief fix] |
| `[Error text]` | [Why it occurs] | [Brief fix] |
| `[Error text]` | [Why it occurs] | [Brief fix] |

## Environment Issues

### Version Mismatches

This module targets:
- **[Tool 1]**: [Version]
- **[Tool 2]**: [Version]

To verify your versions:

```bash
# Check [Tool 1] version
[version check command]

# Check [Tool 2] version
[version check command]
```

### Dependency Conflicts

[Common dependency issues and resolutions]

## Performance Issues

### Slow [Operation]

**Possible causes**:
1. [Cause 1]
2. [Cause 2]

**Solutions**:
- [Solution for cause 1]
- [Solution for cause 2]

## Getting Help

### Official Resources

- [Official Documentation](link)
- [GitHub Issues](link)
- [Community Forum](link)

### Community Support

- [ROS Discourse](https://discourse.ros.org/)
- [Stack Overflow - ROS tag](https://stackoverflow.com/questions/tagged/ros)
- [NVIDIA Developer Forums](https://forums.developer.nvidia.com/)

### Reporting Bugs

When reporting issues, include:

1. Operating system and version
2. Tool versions (ROS 2, Gazebo, etc.)
3. Complete error message
4. Steps to reproduce
5. Expected vs actual behavior

## FAQ

**Q: [Frequently asked question 1]**

A: [Answer]

**Q: [Frequently asked question 2]**

A: [Answer]

**Q: [Frequently asked question 3]**

A: [Answer]
```

## Template Requirements

### Mandatory Elements (FR-022)

1. **Quick Diagnosis Table**: Jump links to common issues
2. **Issue Sections**: Symptom, Cause, Solution format
3. **Error Messages Reference**: Common errors with fixes
4. **Version Information**: Pinned versions per FR-023
5. **Getting Help**: Links to official resources

### Issue Section Format

Each issue MUST include:
- **Symptoms**: Observable behavior
- **Cause**: Root cause explanation
- **Solution**: Step-by-step fix
- **Prevention** (optional): How to avoid

### Quality Checklist

- [ ] All known issues documented
- [ ] Solutions tested and verified
- [ ] Version requirements match FR-023
- [ ] External links validated
- [ ] FAQ addresses common questions
