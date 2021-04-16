using SelfService.Shared;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SelfService.Server.Repository;

namespace SelfService.Server.Controllers
{
    [Authorize(Roles = "Users")]
    [ApiController]
    [Route("[controller]")]
    public class PaymentsController
    {
        private readonly IBillsRepository repository;

        public PaymentsController(IBillsRepository repository)
        {
            this.repository = repository ?? throw new System.ArgumentNullException(nameof(repository));
        }

        [HttpGet]
        [Route("/api/payments")]
        public async Task<IEnumerable<Payment>> GetPayments()
        {
            System.Console.WriteLine("GetPayments...");
            return await this.repository.GetPayments();
        }

        [HttpGet]
        [Route("/api/payments/{yearMonth}")]
        public async Task<IEnumerable<MonthlyPayment>> GetMonthlyPayments(string yearMonth)
        {
            System.Console.WriteLine($"GetMonthlyPayments: {yearMonth}");
            var payments =  await this.repository.GetMonthlyPayments(yearMonth);
            foreach(var payment in payments){
                System.Console.WriteLine($"{payment.Type}:{payment.Number}");
            }
            return payments;
        }
        
    }
}