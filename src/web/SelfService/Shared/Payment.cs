using System;

namespace SelfService.Shared
{
    public class Payment
    {
        public string Name { get; set; }
        public string Type { get; set; }
        public double Amount { get; set; }
        public DateTime Date { get; set; }
        public string Method { get; set; }
        public string User => this.Type;
    }
}
