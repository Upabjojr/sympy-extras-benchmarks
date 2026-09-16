%--------------------------------------------------------------------------
% File     : ARI186_1 : TPTP v9.3.1. Released v5.0.0.
% Domain   : Arithmetic
% Problem  : Integer: Function of two arguments
% Version  : Especial.
% English  : 

% Refs     : [PW06]  Prevosto & Waldmann (2006), SPASS+T
%          : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    : (22) [PW06]

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.25 v9.1.0, 0.12 v8.2.0, 0.25 v7.5.0, 0.20 v7.4.0, 0.00 v6.3.0, 0.14 v6.2.0, 0.50 v6.1.0, 0.56 v6.0.0, 0.57 v5.5.0, 0.56 v5.4.0, 0.62 v5.3.0, 0.60 v5.2.0, 0.83 v5.1.0, 0.80 v5.0.0
% Syntax   : Number of formulae    :    2 (   0 unt;   1 typ;   0 def)
%            Number of atoms       :    3 (   3 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    2 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   2  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    3 (   1 avg)
%            Number arithmetic     :   12 (   0 atm;   1 fun;   9 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    2 (   1   >;   1   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    6 (   1 usr;   4 con; 0-2 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : 
%--------------------------------------------------------------------------
tff(g_type,type,
    g: ( $int * $int ) > $int ).

tff(co1,conjecture,
    ( ! [U: $int,V: $int] : ( g(U,V) = g(U,$sum(V,2)) )
   => ( ( g(3,3) = g(3,4) )
     => ( g(3,2) = g(3,5) ) ) ) ).

%--------------------------------------------------------------------------
