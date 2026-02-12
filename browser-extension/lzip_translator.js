// Pure JavaScript port of L-ZIP translator - matches Python lzip.py precision
const LZIPTranslator = (() => {
  // Symbol replacements with word boundaries (SAFE - won't corrupt identifiers)
  const SYMBOL_MAP = {
    '\\b(and then|followed by|after that|next step)\\b': '|',
    '\\b(and also|as well as|along with|combined with)\\b': '+',
    '\\b(leads to|results in|implies|therefore|thus|consequently)\\b': '=>',
    '\\b(becomes|transforms to|converts to|changes to)\\b': '->'
  };

  // Common abbreviations (telegraphic compression - safe)
  const ABBREVIATIONS = {
    // Numbers - match with optional space
    '\\b(\\d+)\\s*million\\b': '$1M',
    '\\b(\\d+)\\s*billion\\b': '$1B',
    '\\b(\\d+)\\s*thousand\\b': '$1k',
    '\\b(\\d+),?000,?000\\b': '$1M',
    '\\b(\\d+),?000\\b': '$1k',
    '\\bmillion\\b': 'M',
    '\\bbillion\\b': 'B',
    '\\bthousand\\b': 'k',
    // Time
    '\\bseconds?\\b': 's',
    '\\bminutes?\\b': 'm',
    '\\bhours?\\b': 'h',
    '\\bdays?\\b': 'd',
    '\\bweeks?\\b': 'w',
    '\\bmonths?\\b': 'mo',
    '\\byears?\\b': 'y',
    // Tech terms
    '\\bimage\\b': 'img',
    '\\bvideo\\b': 'vid',
    '\\bdocument\\b': 'doc',
    '\\bapplication\\b': 'app',
    '\\bdatabase\\b': 'db',
    '\\brepository\\b': 'repo'
  };

  // Technique keywords - multi-word phrases only
  const TECHNIQUE_KEYWORDS = {
    'step by step': 'THINK:StepByStep',
    'chain of thought': 'THINK:ChainOfThought',
    'output as json': 'OUT:JSON',
    'return json': 'OUT:JSON',
    'as a table': 'OUT:Table',
    'in markdown': 'OUT:Markdown',
    'write code': 'GEN:Code',
    'generate script': 'GEN:Script',
    'bullet points': 'OUT:Bullets',
    'as a list': 'OUT:List',
    'provide list': 'OUT:List'
  };

  // Filler words - remove only obvious redundancy
  const FILLERS = [
    '\\bplease\\b',
    '\\bkindly\\b',
    '\\bfor me\\b',
    '\\bto me\\b',
    '\\bthank you\\b',
    '\\bi would like\\b',
    '\\bif you could\\b',
    '\\bif you can\\b',
    '\\byou can\\b',
    '\\bcan you\\b',
    '\\bcould you\\b'
  ];

  function extractOperators(text) {
    const operators = [];
    let remaining = text.toLowerCase();

    // ACT (persona/role)
    const actPatterns = [
      { regex: /(?:act as|role|persona|assume|be an?)\s+([a-z\s]{2,30}?)(?:[.,;]|and|then|who|that)/i, group: 1 },
      { regex: /\b(senior|expert|professional|experienced)\s+([a-z]+)(?:\s+(developer|engineer|architect|analyst))?/i, group: 2 }
    ];

    for (const { regex, group } of actPatterns) {
      const match = remaining.match(regex);
      if (match) {
        const role = normalizeRole(match[group].trim().slice(0, 40));
        if (role.length > 1) {
          operators.push(`ACT:${role}`);
          remaining = remaining.slice(0, match.index) + ' ' + remaining.slice(match.index + match[0].length);
          break;
        }
      }
    }

    // OBJ (objective)
    const objPatterns = [
      { regex: /(?:your\s+)?(?:objective|goal)\s+(?:is\s+)?(?:to\s+)?([a-z0-9_\s]{2,50}?)(?:[.,;]|and|$)/i, group: 1 },
      { regex: /(?:^|\.\s+)(?:write|create|generate|produce|develop|design|analyze|summarize)\s+(?:an?\s+)?([a-z0-9_\s]{2,45}?)(?:[.,;]|for|with|about)/i, group: 1 }
    ];

    for (const { regex, group } of objPatterns) {
      const match = remaining.match(regex);
      if (match) {
        const objective = shortenTerm(match[group].trim().slice(0, 50));
        if (objective.length > 1) {
          operators.push(`OBJ:${objective}`);
          remaining = remaining.slice(0, match.index) + ' ' + remaining.slice(match.index + match[0].length);
          break;
        }
      }
    }

    // LIM (constraints)
    const limMatch = remaining.match(/(?:limit|restrict|maximum|under|no|without|only)\s+(?:the\s+)?(?:output\s+)?(?:to\s+)?([a-z0-9\s]{2,40}?)(?:[.,;]|and)/i);
    if (limMatch) {
      const constraint = limMatch[1].trim().slice(0, 40);
      if (constraint.length > 1) {
        operators.push(`LIM:${constraint}`);
        remaining = remaining.slice(0, limMatch.index) + ' ' + remaining.slice(limMatch.index + limMatch[0].length);
      }
    }

    // OUT (output format)
    const outPatterns = [
      /(?:output|format|return|provide|should be)\s+(?:as\s+)?(?:an?\s+)?([a-z\s]{2,40}?)(?:[.,;]|$)/i,
      /use\s+([a-z]+)\s+(?:formatting|format|markup|style|structure)\b/i,
      /formatted?\s+as\s+(?:an?\s+)?([a-z\s]{2,40}?)(?:[.,;]|$)/i
    ];

    for (const regex of outPatterns) {
      const match = remaining.match(regex);
      if (match) {
        const outputFormat = normalizeOutput(match[1].trim().slice(0, 40));
        if (outputFormat.length > 1) {
          operators.push(`OUT:${outputFormat}`);
          remaining = remaining.slice(0, match.index) + ' ' + remaining.slice(match.index + match[0].length);
          break;
        }
      }
    }

    // Technique keywords
    for (const [keyword, operator] of Object.entries(TECHNIQUE_KEYWORDS)) {
      const regex = new RegExp('\\b' + keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'i');
      if (regex.test(remaining)) {
        operators.push(operator);
        remaining = remaining.replace(regex, '');
      }
    }

    return { operators, remaining: remaining.replace(/\s+/g, ' ').trim() };
  }

  function normalizeRole(role) {
    const roleMap = {
      'senior developer': 'Senior_Dev',
      'data scientist': 'Data_Scientist',
      'software architect': 'Software_Architect',
      'machine learning': 'ML',
      'expert': 'Expert',
      'developer': 'Dev',
      'engineer': 'Engineer',
      'architect': 'Architect'
    };

    for (const [key, val] of Object.entries(roleMap)) {
      if (role.includes(key)) return val;
    }
    return role.replace(/\s+/g, '_').replace(/\b\w/g, l => l.toUpperCase());
  }

  function shortenTerm(term) {
    term = term.replace(/\b(a|an|the)\b\s+/gi, '');
    const words = term.split(/\s+/).filter(w => w.length > 2 || /^(ai|ui|ux|db|id|io)$/i.test(w));
    return words.map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('_');
  }

  function normalizeOutput(output) {
    const outputMap = {
      'json': 'JSON',
      'csv': 'CSV',
      'table': 'Table',
      'markdown': 'Markdown',
      'html': 'HTML',
      'code': 'Code',
      'list': 'List'
    };

    for (const [key, val] of Object.entries(outputMap)) {
      if (output.toLowerCase().includes(key)) return val;
    }
    return output.split(/\s+/).map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('+');
  }

  function compressPhrases(text) {
    let result = text;

    // Apply abbreviations
    for (const [pattern, replacement] of Object.entries(ABBREVIATIONS)) {
      result = result.replace(new RegExp(pattern, 'gi'), replacement);
    }

    // Apply symbol map
    for (const [pattern, replacement] of Object.entries(SYMBOL_MAP)) {
      result = result.replace(new RegExp(pattern, 'gi'), replacement);
    }

    // Remove fillers
    for (const filler of FILLERS) {
      result = result.replace(new RegExp(filler, 'gi'), '');
    }

    return result.replace(/\s+/g, ' ').trim();
  }

  function compress(text) {
    if (!text || !text.trim()) return '';

    // Step 1: Compress phrases
    let processed = compressPhrases(text);

    // Step 2: Extract operators
    const { operators, remaining } = extractOperators(processed);

    // Step 3: Build final L-ZIP
    let result;
    if (operators.length > 0 && remaining) {
      result = operators.join(' ') + ' ' + remaining;
    } else if (operators.length > 0) {
      result = operators.join(' ');
    } else {
      result = remaining || processed;
    }

    return `IN:compressed-with-L-ZIP ${result} OUT:expanded-original-text`;
  }

  function expand(text) {
    if (!text) return '';

    let result = text;
    result = result.replace(/^IN:compressed-with-L-ZIP\s+/i, '');
    result = result.replace(/\s+OUT:expanded-original-text$/i, '');

    // Reverse operator replacements
    result = result.replace(/ACT:(\w+)/g, 'Act as $1');
    result = result.replace(/OBJ:(\w+)/g, 'Objective: $1');
    result = result.replace(/LIM:(\w+)/g, 'Limit: $1');
    result = result.replace(/OUT:(\w+)/g, 'Output format: $1');
    result = result.replace(/THINK:(\w+)/g, '$1');
    result = result.replace(/GEN:(\w+)/g, 'Generate $1');

    // Reverse symbol replacements
    result = result.replace(/=>/g, 'leads to');
    result = result.replace(/\|/g, 'and then');
    result = result.replace(/\b(\d+)k\b/gi, '$1000');
    result = result.replace(/\b(\d+)M\b/g, '$1 million');
    result = result.replace(/\bimg\b/g, 'image');
    result = result.replace(/\bvid\b/g, 'video');
    result = result.replace(/\bdoc\b/g, 'document');
    result = result.replace(/\bapp\b/g, 'application');
    result = result.replace(/\bdb\b/g, 'database');
    result = result.replace(/\brepo\b/g, 'repository');

    return result;
  }

  return { compress, expand };
})();
