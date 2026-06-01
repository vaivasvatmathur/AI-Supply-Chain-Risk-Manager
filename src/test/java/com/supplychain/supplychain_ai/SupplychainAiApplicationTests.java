package com.supplychain.supplychain_ai;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;

@SpringBootTest
@TestPropertySource(properties = "spring.task.scheduling.enabled=false")
class SupplychainAiApplicationTests {

	@Test
	void contextLoads() {
	}

}
