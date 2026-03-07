package com.supplychain.supplychain_ai.controller;

import com.supplychain.supplychain_ai.entity.RiskAlert;
import com.supplychain.supplychain_ai.repository.RiskAlertRepository;
import com.supplychain.supplychain_ai.service.RiskService;

import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/risk")
public class RiskController {

    private final RiskAlertRepository riskAlertRepository;
    private final RiskService riskService;

    public RiskController(RiskAlertRepository riskAlertRepository,
                          RiskService riskService) {
        this.riskAlertRepository = riskAlertRepository;
        this.riskService = riskService;
    }

    @GetMapping
    public List<RiskAlert> getRiskAlerts() {
        return riskAlertRepository.findAll();
    }

    @PostMapping("/detect")
    public String detectRisks() {
        riskService.detectRisks();
        return "Risk detection executed";
    }
}