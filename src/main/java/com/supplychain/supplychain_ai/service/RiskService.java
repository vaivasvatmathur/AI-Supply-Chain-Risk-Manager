package com.supplychain.supplychain_ai.service;

import com.supplychain.supplychain_ai.entity.Order;
import com.supplychain.supplychain_ai.entity.RiskAlert;
import com.supplychain.supplychain_ai.repository.OrderRepository;
import com.supplychain.supplychain_ai.repository.RiskAlertRepository;

import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class RiskService {

    private final OrderRepository orderRepository;
    private final RiskAlertRepository riskAlertRepository;

    public RiskService(OrderRepository orderRepository,
                       RiskAlertRepository riskAlertRepository) {
        this.orderRepository = orderRepository;
        this.riskAlertRepository = riskAlertRepository;
    }

    public void detectRisks() {

        List<Order> orders = orderRepository.findAll();

        for (Order order : orders) {

            if (order.getExpectedDelivery() != null &&
                order.getExpectedDelivery().isBefore(LocalDate.now())) {

                RiskAlert alert = new RiskAlert();

                alert.setOrderId(order.getId());
                alert.setRiskScore(0.8);
                alert.setReason("Delivery delay detected");
                alert.setTimestamp(LocalDateTime.now());

                riskAlertRepository.save(alert);
            }
        }
    }
}