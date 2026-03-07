package com.supplychain.supplychain_ai.service;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class MonitoringAgent {

    private final RiskService riskService;

    public MonitoringAgent(RiskService riskService) {
        this.riskService = riskService;
    }

    @Scheduled(fixedRate = 30000)
    public void monitorSupplyChain() {

        System.out.println("AI Agent scanning supply chain...");

        riskService.detectRisks();

        System.out.println("Risk detection completed.");
    }
}