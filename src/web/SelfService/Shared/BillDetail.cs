using System;

namespace SelfService.Shared
{
    public class BillDetail
    {
        public string Type { get; set; }
        public string Number { get; set; }
        public string Name { get; set; }
        public string Primary { get; set; }
        public decimal PlanAmount { get; set; }
        public decimal Equipment { get; set; }
        public decimal Services { get; set; }
        public decimal OneTimeCharge { get; set; }
        public decimal Total { get; set; }
        public bool IsAbovePlan => (this.Total - this.PlanAmount) > 5.0m;
        public bool IsPaid { get; set; }
    }
}