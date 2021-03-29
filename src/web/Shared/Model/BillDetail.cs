namespace web.Shared.Model
{
    internal class BillDetail
    {
        public string Type {get; set;}
        public string Number {get; set;}
        public string Name {get; set;}
        public string Primary {get; set;}
        public decimal PlanAmount {get; set;}
        public decimal Equipment {get; set;}
        public decimal Services {get; set;}
        public decimal OneTimeCharge {get; set;}
        public decimal Total {get; set;}
    }
}