Moritz Natalini — Professional Context Document
1. Profile

Name: Moritz Natalini
Role: Product / Monetisation Leader — Ads & Partnerships
Company: ESL FACEIT Group (EFG)
Area: Advertising, Brand Partnerships, Monetisation Products, Engagement Systems

Moritz leads initiatives that monetise user engagement within the FACEIT ecosystem, primarily through:

Advertising formats

Brand integrations

Partner activations

Engagement-driven monetisation products

His work sits at the intersection of:

Product

Commercial / Partnerships

Engineering

Data

Privacy / Legal

The goal is to increase revenue per user while preserving player engagement and trust.

2. Company & Platform Context
ESL FACEIT Group (EFG)

EFG operates competitive gaming ecosystems including:

FACEIT platform

CS2 / Counter-Strike competitive matchmaking

Esports tournaments

Player engagement systems

FACEIT is a highly engaged gaming platform with users playing matches and interacting with content, rewards, and partner activations.

Key monetisation pillars include:

Subscriptions

Brand partnerships

Advertising

Partner conversions (e.g. betting / trading platforms)

3. Core Product Areas Moritz Works On
3.1 Advertising Platform

Ad inventory across FACEIT properties.

Formats

Display ads

Outstream video

Interstitial video

Skin ads

Native placements

Mission-based brand activations

Infrastructure

Key components include:

Google Ad Manager (GAM)

Prebid

Header bidding integrations

Publisher partners

Refresh logic

Current refresh logic:

Refresh every 30 seconds

Implemented historically in front-end

Publift sometimes overrides the logic

Goal:

Move refresh logic from FE to GAM

Enable ad-unit level control

Increase flexibility

Reduce engineering dependency

3.2 Engagement Engine

A core system designed to drive user actions that produce monetisable events.

Examples:

Missions

Rewards

Progression mechanics

Partner activations

The Engagement Engine drives:

player actions

reward loops

monetisation triggers

It connects players to:

partners

premium features

reward systems

3.3 FACEIT Missions

One of the most important engagement monetisation tools.

What Missions Do

They incentivise users to:

play matches

complete tasks

interact with partners

convert into partner actions

Examples of tasks:

Play matches

Deposit with a partner

Pass KYC

Make trades

Complete weekly progression

Rewards

Users receive:

FACEIT points

skins

partner rewards

premium tier progression

3.4 Loyalty / Tier Progression

Used especially in high value partner campaigns.

Example tier progression:

Subscriber

Gold

Platinum

Diamond

Elite

Legend

Used to drive:

repeated deposits

weekly engagement

long-term retention

4. Key Strategic Initiative Areas
4.1 Engagement-Driven Monetisation

Strategy:

Transform engagement into monetisable outcomes through:

missions

partner integrations

reward loops

Instead of traditional advertising alone, the platform aims to generate measurable business outcomes for partners.

4.2 Customer Data Platform (CDP)

Goal:

Create better user segmentation and targeting for monetisation.

CDP enables:

audience segmentation

personalised activations

partner targeting

monetisation optimisation

4.3 Account Linkage Strategy

Critical conversion step.

Typical funnel:

FACEIT User
    ↓
Account Linkage
    ↓
KYC
    ↓
Deposit
    ↓
High Value Player

Used heavily with:

betting partners

trading platforms

crypto partners

4.4 New Advertising Verticals

Expansion beyond traditional gaming advertisers.

Potential verticals being validated:

Fast Food

Streaming platforms

Gaming peripherals

Consumer brands

Goal:

Diversify revenue away from only gaming-related advertisers.

5. Major Advertising Experiments
Prebid vs Publisher Platforms

Testing different header bidding solutions.

Key players tested:

Publift

Strengths:

High fill rate

strong demand

Concerns:

lower eCPM

potentially aggressive refresh

Mobalytics

Another provider evaluated.

Tests compare:

fill rate

eCPM

revenue per page view

6. Key Metrics Frameworks

Moritz is highly metrics-driven.

Common metrics include:

Ad Metrics

Impressions

Fill rate

eCPM

CTR

Viewability

Revenue per page view

Engagement Metrics

Matches played

Mission completion rate

Session frequency

Reward redemption

Conversion Metrics

Used for partner campaigns.

Examples:

Account Linkage

KYC completion

Deposits

Trades

Example scoring weights used:

AL = 3
KYC = 6
Deposit = 9
Advertiser Value Metrics

Moritz is developing internal frameworks including:

AVE (Advertiser Value Efficiency)

Measures how efficiently the platform delivers valuable outcomes to partners.

OVU (Outcome Value Units)

Standardised measurement of partner outcomes.

Example:

1 KYC = X OVU
1 Deposit = Y OVU
1 Trade = Z OVU
North Star Metric (NSM)

Potential North Star concept:

Outcome Value Units per Active Player

This aligns platform engagement with advertiser value creation.

7. Key Business Cases Moritz Is Working On
Interstitial Video Ads

Concept:

show 1 video per user per day

Example modelling:

Video CPM: $15
Users exposed daily: X
Revenue = impressions × CPM

This is primarily a behavioural tolerance test rather than a monetisation test.

Objective:

Validate whether users tolerate the format without harming engagement or increasing ad-block usage.

8. Rollout Strategy Philosophy

Moritz prefers phased rollouts to mitigate business risk.

Typical rollout pattern:

Phase 1

Small countries / low revenue risk.

Purpose:

validate behaviour

validate UX

Phase 2

Medium-sized markets.

Purpose:

refine monetisation

validate metrics

Phase 3

Tier 1 markets.

Purpose:

scale revenue

9. Constraints & Platform Limitations

Example:

GAM Limitation

Google Ad Manager does not operate in Russia, meaning Russia cannot be included in certain tests.

Premium Inventory Strategy

Certain high value ad placements are initially sold through:

direct deals

not programmatic

Especially for:

Tier 1 countries

premium video inventory

10. Key Partners Mentioned
Betting / Trading / Conversion Partners

Winline

Tradeit

Whitebit

Paysafe

These partners drive:

deposits

trades

KYC verification

Advertising / Monetisation Partners

Publift

Mobalytics

Google Ad Manager

Potential advertiser verticals

Fast food brands

Streaming platforms

Gaming hardware brands

11. Internal Stakeholders

People frequently referenced:

Leadership

President of FACEIT

SVP Product

Product / Engineering

Mandar

Ilya

Reece

Teo

Eugene Zelenyi

Commercial / Partnerships

Adam Goh

Claire

Isabel Diezma

Jamie Fitzgerald

William Seghers

Privacy / Legal

Julia

Gina

Privacy is particularly relevant for:

data sharing with partners

KYC data

cross-product data reuse

12. Privacy & Legal Considerations

Certain partner deals involve data exchange, especially where partners require:

identity verification

conversion tracking

Example issue:

Privacy team reviewing whether FACEIT can exchange data with Paysafe.

Even though similar exchanges already happen with:

Whitebit

Tradeit

Contracts may need to explicitly allow data reuse across partners.

13. Monetisation Philosophy

Moritz focuses on:

Outcome-driven monetisation

Rather than pure impressions.

Example:

Traditional ads → CPM revenue
FACEIT approach → user outcomes

Outcomes include:

deposits

trades

verified accounts

Engagement-first monetisation

Core principle:

Engagement drives monetisation.

This means validating user tolerance first, then scaling monetisation.

14. Example Data Analyses Moritz Performs

Typical analysis tasks include:

Revenue per page view

Experiment comparison

Tier 1 vs Tier 2 vs Tier 3 performance

Conversion funnels

Partner campaign performance

Often using:

spreadsheets

A/B tests

cohort analysis

15. Long-Term Roadmap Vision

Multi-year roadmap:

Phase 1 (2024)

Foundations

monetisation infrastructure

mission systems

engagement loops

Phase 2 (2025)

Optimisation

targeting improvements

better conversion funnels

partner integrations

Phase 3 (2026–2027)

Expansion

new advertiser verticals

outcome-based advertising

deeper engagement monetisation

16. Summary

Moritz Natalini leads monetisation innovation within FACEIT by combining:

advertising technology

engagement systems

partner conversions

user reward mechanics

His work focuses on turning player engagement into measurable advertiser outcomes while maintaining a healthy player experience.