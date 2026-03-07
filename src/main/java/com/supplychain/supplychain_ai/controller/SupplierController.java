package com.supplychain.supplychain_ai.controller;

import com.supplychain.supplychain_ai.entity.Supplier;
import com.supplychain.supplychain_ai.repository.SupplierRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/suppliers")
public class SupplierController {

    private final SupplierRepository supplierRepository;

    public SupplierController(SupplierRepository supplierRepository){
        this.supplierRepository = supplierRepository;
    }

    @GetMapping
    public List<Supplier> getAllSuppliers(){
        return supplierRepository.findAll();
    }

    @PostMapping
    public Supplier createSupplier(@RequestBody Supplier supplier){
        return supplierRepository.save(supplier);
    }
}