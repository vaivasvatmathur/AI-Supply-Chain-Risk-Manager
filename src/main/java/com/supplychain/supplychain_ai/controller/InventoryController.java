package com.supplychain.supplychain_ai.controller;

import com.supplychain.supplychain_ai.entity.Inventory;
import com.supplychain.supplychain_ai.repository.InventoryRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/inventory")
public class InventoryController {

    private final InventoryRepository inventoryRepository;

    public InventoryController(InventoryRepository inventoryRepository){
        this.inventoryRepository = inventoryRepository;
    }

    @GetMapping
    public List<Inventory> getInventory(){
        return inventoryRepository.findAll();
    }

    @PostMapping
    public Inventory createInventory(@RequestBody Inventory inventory){
        return inventoryRepository.save(inventory);
    }
}