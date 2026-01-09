# Carrier Lookup Tool - Project Context

## Project Overview
A Python-based tool for performing bulk carrier lookups using the Ytel API. Processes phone numbers in E.164 format and enriches them with carrier information including network provider, line type, location data, and more.

## Key Project Goals
1. **Bulk Processing**: Handle large volumes of phone numbers efficiently (up to 540,000/hour at 150 TPS)
2. **Rate Limiting**: Respect API limits to avoid throttling (configurable, default 10 TPS)
3. **Data Enrichment**: Add carrier, line type, city, state, zip code, and country data
4. **Error Handling**: Graceful handling with detailed error messages in output CSV
5. **Privacy**: Never commit API keys or personal phone numbers to version control

## Security & Privacy Requirements
- **CRITICAL**: Never include personal phone numbers in code or documentation
  - User's personal number (949-310-1364) must never appear in any files
  - Use generic 555-prefix numbers for examples
- **API Key Security**: 
  - Store in `.env.ytel` file (gitignored)
  - Never commit to repository
  - Refer user to 1Password for LLM keys when needed

## Current Configuration
- **Default Rate Limit**: 10 TPS (36,000 numbers/hour)
- **Input File**: `phone_numbers.csv` (E.164 format with + prefix)
- **Output File**: `phone_numbers_with_carrier.csv`
- **API**: Ytel Carrier Lookup API v4

## Processing Capacity (Per Hour)
- 1 TPS: 3,600 numbers
- 10 TPS: 36,000 numbers (default)
- 50 TPS: 180,000 numbers
- 100 TPS: 360,000 numbers
- 150 TPS: 540,000 numbers

## GitHub Repository
- **Owner**: k7cfo
- **Repo Name**: Carrier-Lookup-Tool
- **URL**: https://github.com/k7cfo/Carrier-Lookup-Tool
- **License**: MIT

## File Structure
```
get-carrier/
├── carrier_lookup.py          # Main script
├── phone_numbers.csv          # Input file (E.164 format)
├── phone_numbers_with_carrier.csv  # Output (generated)
├── requirements.txt           # Dependencies (requests, python-dotenv)
├── .env.ytel                  # API key (gitignored)
├── .env.ytel.example         # Example template
├── .gitignore                # Excludes .env.ytel, output CSV, etc.
├── LICENSE                   # MIT License
├── README.md                 # Full documentation
└── WARP.md                   # This file
```

## Key Code Components
- **Rate Limiting**: `RATE_LIMIT` variable controls TPS (line 30)
- **API Endpoint**: `https://api.ytel.com/api/v4/carrier/lookup`
- **Phone Format**: E.164 (+1XXXXXXXXXX for US numbers)
- **Error Logging**: All errors captured in output CSV with details

## Common Operations

### Making Changes to Rate Limit
Edit `carrier_lookup.py` line 30:
```python
RATE_LIMIT = 10  # Change this value (ensure API plan supports it)
```

### Adding New Features
- Always verify against Ytel API documentation first
- Use Context7 MCP server for official API docs when needed
- Test with small sample before bulk processing
- Update README if behavior changes

### Git Workflow
- Commit messages should include: `Co-Authored-By: Warp <agent@warp.dev>`
- Never force push unless correcting security issues
- Always check for sensitive data before committing

## Important Notes
- Phone numbers must be in E.164 format (+country code)
- Random phone numbers may not be valid/assigned and can fail lookup
- Output CSV includes raw API response for debugging
- Tool respects API rate limits with built-in delays

## Testing Considerations
- Test rate limit changes with small batches first
- Monitor API usage to avoid unexpected charges
- Verify output CSV format after changes
- Check for SSL/TLS warnings (usually harmless)

## Future Enhancements to Consider
- Support for international number formats beyond North America
- Batch API calls if Ytel supports it
- Progress saving/resume capability for large jobs
- Enhanced error retry logic
- Database output option in addition to CSV

## Dependencies
- Python 3.7+
- `requests` library
- `python-dotenv` library
- Ytel API key

## Contact & Support
- GitHub Issues: Use for bug reports and feature requests
- Ytel API Docs: https://api-docs.ytel.com/
