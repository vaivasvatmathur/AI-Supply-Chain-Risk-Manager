package com.supplychain.supplychain_ai.controller;

import com.supplychain.supplychain_ai.entity.Order;
import com.supplychain.supplychain_ai.repository.OrderRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderRepository orderRepository;

    public OrderController(OrderRepository orderRepository){
        this.orderRepository = orderRepository;
    }

    @GetMapping
    public List<Order> getOrders(){
        return orderRepository.findAll();
    }

    @PostMapping
    public Order createOrder(@RequestBody Order order){
        return orderRepository.save(order);
    }
}