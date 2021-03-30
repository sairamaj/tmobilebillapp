using System;

namespace web.Shared.Model
{
    internal class CacheEntry<T>
    {
        public DateTime EntryTime {get; set;}
        public TimeSpan Expiry {get; set;}
        public T Value {get; set;}

        public override string ToString()
        {
            return $"{this.EntryTime} : {this.Expiry}";
        }
    }
}