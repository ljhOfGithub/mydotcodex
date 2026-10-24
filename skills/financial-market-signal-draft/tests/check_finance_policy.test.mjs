import assert from 'node:assert/strict';
import test from 'node:test';

import { scanFinancePolicy } from '../scripts/check_finance_policy.mjs';

test('allows ordinary sourced market analysis', () => {
  const text = '本文比较能源股与原油价格，只整理公开信息，不构成投资建议。';
  assert.deepEqual(scanFinancePolicy(text), []);
});

test('blocks crypto topics even without a service or recommendation', () => {
  assert.equal(
    scanFinancePolicy('加密资产周末仍在交易，美股市场处于休市状态')[0].id,
    'platform-risk-crypto-topic',
  );
  assert.equal(scanFinancePolicy('Bitcoin weekend market note')[0].id, 'platform-risk-crypto-topic');
});

test('blocks illegal currency services', () => {
  assert.equal(scanFinancePolicy('提供私下换汇服务')[0].id, 'illegal-currency-service');
});

test('blocks credit cashout services', () => {
  assert.equal(scanFinancePolicy('可以代办信用卡并提供信用卡套现')[0].id, 'illegal-credit-or-cashout');
});

test('blocks illegal investment services', () => {
  assert.equal(scanFinancePolicy('加入股票推荐群获取荐股服务')[0].id, 'illegal-investment-service');
});

test('blocks noncompliant brokerage commissions', () => {
  assert.equal(scanFinancePolicy('证券开户万一免五')[0].id, 'noncompliant-brokerage');
});

test('does not treat named stocks as a recommendation by itself', () => {
  assert.deepEqual(scanFinancePolicy('文章比较 AAPL 与 MSFT 的财报数据'), []);
});
