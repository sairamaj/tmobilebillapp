namespace web.Shared.Model
{
    internal class Bill
    {
        public string Type { get; set; }
        public decimal Total { get; set; }
        public decimal PerLine {get; set;}
    }
}