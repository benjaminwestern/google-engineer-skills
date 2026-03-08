# Best Practices

Guidelines for creating high-quality skills.

## Content Organization

### By Functionality

Group commands by what they do:

- **Core**: Essential, frequently used commands
- **Management**: Administrative and configuration
- **Utilities**: Helper and diagnostic commands

### By Workflow

Organize by user journey:

- **Setup**: Installation and configuration
- **Operation**: Day-to-day usage
- **Cleanup**: Removal and maintenance

### By Frequency

Prioritize by usage:

- **Common**: Daily operations (Quick Start section)
- **Advanced**: Occasional tasks
- **Rare**: Edge cases and troubleshooting

## Writing Guidelines

### Description Field

- **Length**: 1-1024 characters
- **Format**: `<Action>. Use when you need to <use case>`
- **Example**: "Automates Docker containers for building, running, and deploying. Use when working with Dockerfiles, images, or containerized applications."

### Quick Start Section

- Include 3-5 most common commands
- Make them copy-paste ready
- Cover 80% of typical use cases
- Use comments sparingly within code blocks

### Examples

- Real-world scenarios
- Complete, working commands
- Progressive complexity (simple to advanced)
- Include expected output when helpful

### Command Organization

- Group related commands under clear headers
- Use consistent formatting
- Include brief explanations where needed
- Avoid dumping all commands without context

## Do's and Don'ts

### ✅ Do

- Write action-oriented descriptions
- Provide practical, tested examples
- Use clear, logical category organization
- Include error handling where relevant
- Keep examples concise but complete
- Use consistent terminology

### ❌ Don't

- Use generic descriptions like "A tool for X"
- Provide incomplete snippets
- Create unorganized command lists
- Include irrelevant edge cases
- Duplicate content across sections
- Use jargon without explanation

## Validation Checklist

Before publishing your skill:

- [ ] YAML frontmatter is valid (test with a YAML parser)
- [ ] Name matches directory name exactly
- [ ] Description is under 1024 characters
- [ ] Quick start has working commands
- [ ] Examples are complete and tested
- [ ] Categories are logical and consistent
- [ ] No markdown syntax errors
- [ ] All links are functional
- [ ] Follows repository naming conventions

## Skill Naming Conventions

- Use lowercase with hyphens: `docker-cli`, `k8s-deploy`
- Be specific: `aws-s3-cli` not just `aws`
- Match directory name exactly
- Include version in filename if needed: `terraform-v1.5`
- Avoid generic names: prefer `gcp-cloud-storage` over `storage`

## Testing Your Skill

```bash
# Add the skill locally
npx skills add . --skill <your-skill-name>

# Verify it appears in the list
npx skills list

# Check for any loading errors
npx skills check

# Test the skill content
# (Load it in your AI agent and verify it works as expected)
```

## Troubleshooting

### Content is too long

- Focus on the most common 20% of commands
- Link to external documentation for edge cases
- Use "See also" sections for related topics
- Consider splitting into multiple related skills

### Missing examples

- Check extracted snapshots for hidden examples
- Look for "Getting Started" sections in source docs
- Search for "Example" headers
- Review common Stack Overflow questions

### Unclear organization

- Group by user intent (what they want to do)
- Not by technical category (unless that helps)
- Test with a real task - does it make sense?
- Get feedback from potential users
