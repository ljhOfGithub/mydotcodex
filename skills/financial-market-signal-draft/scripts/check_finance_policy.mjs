#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';

export const policyPatterns = [
  {
    id: 'platform-risk-crypto-topic',
    label: '平台高风险加密资产主题',
    pattern: /加密(?:货币|资产|市场)|数字货币|虚拟币|稳定币|比特币|以太坊|\b(?:crypto|bitcoin|ethereum|btc|eth|usdt|usdc)\b/iu,
  },
  {
    id: 'illegal-currency-service',
    label: '非法货币服务',
    pattern: /非法换外币|私下换汇|代换外币|造假币|制作假币|违规印(?:制)?人民币/u,
  },
  {
    id: 'illegal-credit-or-cashout',
    label: '违规借贷或套现服务',
    pattern: /代办(?:贷款|信用卡)|办理(?:贷款|信用卡)|信用卡套现|帮人背(?:黑账|债|账)|电子借条服务|推销POS机|办理POS机/u,
  },
  {
    id: 'illegal-investment-service',
    label: '违法投资或证券推荐服务',
    pattern: /场外配资|配资炒股|洗钱|跑分|代理退保|代办退保险|荐股荐基|推荐(?:股票|基金|炒股软件)|股票推荐群|基金推荐群/u,
  },
  {
    id: 'noncompliant-brokerage',
    label: '不合规证券佣金活动',
    pattern: /万一免五|低于万一|免五开户|超低股票交易佣金|超低证券佣金/u,
  },
];

export function scanFinancePolicy(text) {
  return policyPatterns.flatMap(({ id, label, pattern }) => {
    const match = text.match(pattern);
    return match ? [{ id, label, keyword: match[0] }] : [];
  });
}

async function main(args) {
  if (args.length === 0) {
    console.error('usage: check_finance_policy.mjs <file> [file...]');
    process.exitCode = 64;
    return;
  }

  const results = [];
  for (const file of args) {
    const text = await readFile(file, 'utf8');
    const violations = scanFinancePolicy(text);
    if (violations.length > 0) results.push({ file, violations });
  }

  console.log(JSON.stringify({ passed: results.length === 0, results }, null, 2));
  if (results.length > 0) process.exitCode = 2;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  await main(process.argv.slice(2));
}
