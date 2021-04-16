using System;
using System.Linq;

namespace SelfService.Shared
{
    public class MonthlyPayment
    {
        public string Type { get; set; }
        public string Number { get; set; }
        public string YearMonth => this.Type.Split('_').First();
    }
}